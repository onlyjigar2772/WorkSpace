#!/tools/swdev/bin/perl5.10.0
#
# latest-build - given a branch, display the latest build version
#
# $Id: latest-build
#

use strict;
use warnings;
use DBI;
use FindBin;
use Getopt::Long;
use Ericsson::Hivemind;
use File::Basename;
use Date::Parse;
use Time::Piece;
use Time::Local;
use POSIX qw(strftime);
use Carp;
use List::MoreUtils qw/ uniq /;

(our $ME = $0) =~ s|.*/||;
our $VERSION = '2.1';

my $config_file   = "/tools/swdev-cmn/etc/config/latest-build/tools.cfg";
my $environment   = "production";
my $block         = "hivemind";
my @branch_ids    = ();
my $result;

# Command-line options
my $debug;
my ($attempt, $success, $failure, $detail ,$show_timestamp);
my ($iso,$unix,$rfc,$epoch,$alltimes);

my $op_success = GetOptions(
  'detail'       => \$detail,
  'attempt'      => \$attempt,
  'success'      => \$success,
  'failure'      => \$failure,
  'timestamp'    => \$show_timestamp,
  'iso8601'      => \$iso,
  'date'         => \$unix,
  'rfc2822'      => \$rfc,
  'epoch'        => \$epoch,
  'alltimes'     => \$alltimes,

  'environment=s'=> \$environment,
  'config_file=s'=> \$config_file,
  'debug'        => \$debug,
  'help'         => sub{ usage(0) },
  'version'      => sub { print "\n$ME version $VERSION\n\n"; exit 0 },
) or usage(1);

if ( !$op_success ) {
  usage(1);
}

if ( !defined( $environment ) || !defined( $config_file ) ) {
  usage(1);
}

$show_timestamp=1  if ($unix || $iso || $rfc || $epoch);

my $hapi = new Ericsson::Hivemind(config_file => $config_file,
                                  environment => $environment,
                                  block       => $block );
my $dbh = $hapi->connect();

$detail = 1 if ($alltimes);

# Fetch command-line arguments.  Barf if too many.
my ($repo, $branch_name) = get_repo_branch();

if ( !defined($repo) ) {
   # repo_name not specified in command so look it up
   @branch_ids = get_branch_id_by_branch_name($branch_name);
   my $branches_found = @branch_ids;

   if ( $branches_found == 2 ) {
     # check for successor
     if ( ! check_successor(@branch_ids) ) {
       print "Found $branches_found occurences of $branch_name in database. "
           . "Please specify the repo name.\n";
       display_duplicates(@branch_ids);
       exit 1;
     }
   } elsif ( $branches_found > 2 ) {
     print "Found $branches_found occurences of $branch_name in database. "
         . "Please specify the repo name.\n";
     display_duplicates(@branch_ids);
     exit 1;
   } elsif ( $branches_found == 0 ) {
     print "$branch_name branch not found. This branch might be set to inactive.\n";
     exit 1;
   }
} elsif ( defined($branch_name) ) {
   @branch_ids = get_branch_id_by_branch_and_repo($branch_name, $repo);
   if ( scalar @branch_ids == 0 ) {
     print "$branch_name branch in $repo repo not found. "
         . "This branch might be set to inactive.\n";
     exit 1;
   } elsif ( scalar @branch_ids > 1 ) {
     print "More than one occurence of $branch_name branch in $repo repo found. "
          . "Please specify the repo name.\n";
     display_duplicates(@branch_ids);
     exit 1;
   }
} else {
  usage(1);
}

my $and_clause = "";
if ($attempt) {
  $and_clause = '';
} elsif ($failure) {
  $and_clause = "AND b.build_outcome = 'ERROR'";
} else {
  $and_clause = "AND b.build_outcome IN ('SUCCESS','WARNING')";
}
my ($release,$sha,$build_time,$build_outcome,$product_id,$repo_vcs,$repo_name) =
                get_latest_build_by_branch_id(\@branch_ids, $and_clause);

# ------- printing result
if (defined $release) {
  $result->{repo_vcs}      = $repo_vcs;
  $result->{release}       = $release;
  $result->{build_time}    = $build_time;
  $result->{build_outcome} = $build_outcome;
  $result->{sha} = $sha;
  if (defined $product_id) {
    $result->{product} = get_product_by_id($product_id);
  } else {
    $result->{product} = 'unknown';
  }
  if (1) {
    print_result_detail();
  } elsif ($show_timestamp) {
    print_result_timestamp();
  } else {
    print "$result->{release}\n";
  }
} else {
  print_no_result();
}

$hapi->disconnect();
exit(0);

# --------------- print_no_result
sub print_no_result {
    #my $argStr = join (" ", @ARGV);
    #print "\nSorry, there is no build for '$argStr'\n";
    if ( defined($repo) ) {
      print "No builds found for $branch_name branch in $repo repo.\n";
    } else {
      print "No builds found for $branch_name branch\n";
    }
} # print_no_result

# --------------- usage
sub usage {
  my $status = shift;
  if ( !defined $status ) {
    die "$ME Error: No parameter provided to usage()\n";
  }

  print  <<"END_USAGE";

Usage: $ME [OPTIONS] Repo and/or Branch

$ME displays the most recent build version of REPO and/or BRANCH

    % $ME --timestamp packet
    12.1.10.0.12  Sun May 20 00:01:40 2012

    % $ME -detail swfeature_int
    Product      : SmartEdge
    Build        : swfeature_int-12.1.10.100.223
    Build Time   : Fri May 18 12:00:21 PDT 2012
    Repo         : cvsroot
    Branch       : swfeature_int
    Build Status : SUCCESS

    % $ME --detail swfeature_int.git master
    Product      : SmartEdge
    Build        : 13.2.15.100.56
    Build Time   : Thu Feb 07 11:05:13 2013
    Repo         : swfeature_int.git
    Branch       : master
    Build Status : SUCCESS
    SHA          : 7479952af0fea7318143557ef4c3469d74fa1931

OPTIONS:

  --timestamp display build timestamp
  --detail    display detail of the release
  --success   dipslay latest success/warning build  (default)
  --attempt   display latest attempt build no matter the outcome
  --failure   display latest failure build

  --date      timestamp format: e.g. Mon Apr 16 16:00:17 PDT 2012 (default)
  --iso8601   timestamp format: e.g. 2012-04-16T16:00:17-0700,
  --rfc2822   timestamp format: e.g. Mon Apr 16 16:00:17 2012 -0700
  --epoch     timestamp format: e.g. 1334617217
  --alltimes  timestamps in all these 4 formats.

  --help      display this message
  --version   display program name and version

END_USAGE
  exit $status;
} # usage

# ----------------- get_repo_branch
sub get_repo_branch {
  my $repo_name = undef;
  my $branch_name = undef;

  if ( scalar @ARGV == 1 ) {
    $branch_name = $ARGV[0];
  } elsif ( scalar @ARGV == 2 ) {
    $repo_name = $ARGV[0];
    $branch_name = $ARGV[1];

  } else {
    print "Invalid number of arguments.\n";
    usage(1);
  }

  return ($repo_name, $branch_name);

} # get_repo_branch

sub check_successor {
  my @branch_ids = @_;
  my $sql = qq {
    SELECT * FROM vcs.branch_successor WHERE
    ( src_branch_id = ? AND dst_branch_id = ? ) OR
    ( dst_branch_id = ? AND src_branch_id = ? )
  };
  my $sth = $dbh->prepare($sql);
  $sth->execute($branch_ids[0], $branch_ids[1], $branch_ids[0], $branch_ids[1]);
  $sth->fetch();
  return $sth->rows();
}

sub get_branch_id_by_branch_name {
  my $branch_name = shift;
  my $branch_id = undef;
  my $branch_ids = ();
  my @data = ();
  my $sql = qq {
    SELECT branch_id FROM vcs.branch WHERE branch_name = ?
  };
  my $sth = $dbh->prepare($sql);
  $sth->execute($branch_name);
  while ( @data = $sth->fetchrow_array() ) {
    push (@branch_ids, $data[0]);
  }
  return @branch_ids;
}

sub get_branch_id_by_branch_and_repo {
  my $branch_name = shift;
  my $repo_name = shift;
  my $branch_id = undef;
  my $branch_ids = ();
  my @data = ();
  my $sql = qq {
    SELECT b.branch_id FROM vcs.branch b
    INNER JOIN vcs.repo r ON r.repo_id = b.repo_id
    WHERE b.branch_name = ?
    AND r.repo_name = ?
    AND b.branch_status = 'active'
  };
  my $sth = $dbh->prepare($sql);
  $sth->execute($branch_name, $repo_name);
  while ( @data = $sth->fetchrow_array() ) {
    push (@branch_ids, $data[0]);
  }
  return @branch_ids;
}

sub display_duplicates {
  my $branch_ids = @_;
  my @data = ();
  my $sql = qq {
    SELECT p.hm_name, br.branch_name, r.repo_name
    FROM vcs.branch br
    INNER JOIN vcs.branch_product bp ON bp.branch_id = br.branch_id
    INNER JOIN product p ON p.id = bp.product_id
    INNER JOIN vcs.repo r ON r.repo_id = br.repo_id
    WHERE br.branch_status = 'active'
    AND br.branch_id = ?
  };
  my $sth = $dbh->prepare($sql);
  print "\n  Product, branch, repo\n";
  print "  ---------------------\n";
  foreach my $branch_id (@branch_ids) {
    $sth->execute($branch_id);
    while ( @data = $sth->fetchrow_array() ) {
      print "  $data[0], $data[1], $data[2]\n";
    }
  }
}

# -------------------- get_product_by_id
sub get_product_by_id {
  my $product_id = shift;
  my @results = ();

  my $sql = qq {
    SELECT hm_name
    FROM public.product
    WHERE id = $product_id
  };

  printDebug("$sql");
  my ($product) = @{$dbh->selectcol_arrayref($sql)};
  return $product;

} # get_product_by_id

# -------------------- get_latest_build_by_branch_id
sub get_latest_build_by_branch_id {
  my ($branch_ids,$and_clause) = @_;
  my @results = ();

  my $sql = "
    SELECT  b.release,
        b.sha,
        b.build_time,
        b.build_outcome,
        b.product_id,
        r.repo_vcs,
        r.repo_name
    FROM public.build b
    INNER JOIN vcs.branch br on br.branch_id = b.branch_id
    INNER JOIN vcs.repo r on r.repo_id = br.repo_id
     WHERE b.branch_id in (" . join(',', ('?') x @$branch_ids) . ")
       AND b.build_time is NOT NULL
       $and_clause
    ORDER BY b.build_time DESC, b.release DESC LIMIT 1 ";

  printDebug("$sql");
  my $sth = $dbh->prepare($sql);
  $sth->execute(@$branch_ids);
  my ($release,$sha,$build_time,$build_outcome,$product_id,$repo_vcs,$repo_name) =
                                                  $sth->fetchrow_array();
  return ($release,$sha,$build_time,$build_outcome,$product_id,$repo_vcs,$repo_name);
} #  get_latest_buld_for_branch_id

# ------------------ get_display_alltimes
sub get_display_alltimes {
    my $utcTime = shift;
    my $offhours = strftime("%z", localtime());
    my $dt_iso = localtime(str2time($utcTime, 'UTC'))->datetime . $offhours;
    my $dt_rfc = (strftime("%a %b %d %H:%M:%S %Y ",
                    localtime(str2time($utcTime, 'UTC')))) . $offhours;
    my @tt = localtime(str2time($utcTime, 'UTC'));
    my $dt_epoch = timelocal(@tt);
    my $dt_unix = strftime("%a %b %d %H:%M:%S %Z %Y",
                    localtime(str2time($utcTime, 'UTC')));
    return ($dt_iso,$dt_unix,$dt_rfc,$dt_epoch);
} # get_display_alltimes

# ------------------ get_displayDT
sub get_displayDT {
    my $utcTime = shift;
    my $dt;
    if ($iso) {
      my $offhours = strftime("%z", localtime());
      $dt = localtime(str2time($utcTime, 'UTC'))->datetime . $offhours;
    } elsif ($rfc) {
      my $offhours = strftime("%z", localtime());
      $dt = (strftime("%a %b %d %H:%M:%S %Y ",
                    localtime(str2time($utcTime, 'UTC')))) . $offhours;
    } elsif ($epoch) {
      my @tt = localtime(str2time($utcTime, 'UTC'));
      $dt = timelocal(@tt);
    } elsif ($unix) {
      # -- unit date
      $dt = strftime("%a %b %d %H:%M:%S %Z %Y",
                    localtime(str2time($utcTime, 'UTC')));
    } else {
      $dt = strftime("%a %b %d %H:%M:%S %Y",
                    localtime(str2time($utcTime, 'UTC')));
    }
    return $dt;

} # get_displayDT

# --------------------- print_result_detail
sub print_result_detail {
  my $headingLen = length("Branching Point") + 1;
  printf("\n%-${headingLen}s: %s", "Repo", $repo_name);
  printf("\n\n%-${headingLen}s: %s", "Branch", $branch_name);
  printf("\n\n%-${headingLen}s: %s", "Product", $result->{product});
  printf("\n\n%-${headingLen}s: %s", "Latest Build",
                                   $result->{release});
  my $utcTime = $result->{build_time};
  if ($alltimes) {
    my ($dt_iso, $dt_unix, $dt_rfc, $dt_epoch) =
                                    get_display_alltimes($utcTime);
    printf("\n%-${headingLen}s ", "Build Time");
    printf("\n%-${headingLen}s: %s", " - ISO 8601", $dt_iso);
    printf("\n%-${headingLen}s: %s", " - Unix date", $dt_unix);
    printf("\n%-${headingLen}s: %s", " - RFC 2822", $dt_rfc);
    printf("\n%-${headingLen}s: %s", " - Epoch", $dt_epoch);
  } else {
    my $displayDT = get_displayDT($utcTime);
    printf("\n\n%-${headingLen}s: %s", "Build Time", $displayDT);
  }
  printf("\n\n%-${headingLen}s: %s", "Build Status", $result->{build_outcome});
  # if ($result->{repo_vcs} eq 'git') {
  #  if (defined $result->{sha}) {
  #   printf("\n%-${headingLen}s: %s", "SHA", $result->{sha});
  # } else {
  #   printf("\n%-${headingLen}s: %s", "SHA", "N/A");
  # }
  # }
  #print "\n";
  my @bid = get_branch_id_by_branch_name($branch_name);
  my @branch_parent = uniq get_parent_id($branch_name);
  my @created_ts = get_created_ts ($bid[0]);
  my @branch_type = get_branch_type($bid[0]);
  #print "\nBranch Type  : $branch_type[0]";
  printf("\n\n%-${headingLen}s: %s", "Branch Type", $branch_type[0]);
  my @branch_status = get_branch_status($bid[0]);
  #print "\n\nBranch Status: $branch_status[0]\n";
  printf("\n\n%-${headingLen}s: %s", "Branch Status", $branch_status[0]);
  if ( scalar @branch_parent == 0 || $branch_parent[0] == $bid[0]){
    printf("\n\n%-${headingLen}s: %s", "Branching Point", "No Parent");
    printf("\n\n%-${headingLen}s: %s", "Parent Branch", "No Parent");
  }
  else {
    #print "\n Parent ID : @branch_parent --- Branch ID : @bid \n";
    my @bdrelease = uniq get_bdrelease_by_time($created_ts[0], @branch_parent);
    if ( scalar @bdrelease < 2) {
      printf("\n\n%-${headingLen}s: %s", "Branching Point", "NA");
      my @pname = get_branch_name_by_branch_id ($branch_parent[0]);
      printf("\n\n%-${headingLen}s: %s, Pulled from Version %s at %s", "Parent Branch", $pname[0], "NA", $created_ts[0]);
    }
    else {
    #print "\n @bdrelease --- $branch_parent[0] --- $created_ts[0] \n";
    #print "\nBranching Point: $bdrelease[0]";
    printf("\n\n%-${headingLen}s: %s", "Branching Point", $bdrelease[0]);
    my @pname = get_branch_name_by_branch_id ($bdrelease[1]);
    #print "\n\nParent Branch: $pname[0], Pulled from Version $bdrelease[0] at $created_ts[0]";
    printf("\n\n%-${headingLen}s: %s, Pulled from Version %s at %s", "Parent Branch", $pname[0], $bdrelease[0], $created_ts[0]);
    }
  }
my $locked_status = `branch-locked $branch_name`;
#print "\n\nLocked status: $locked_status ";
printf("\n\n%-${headingLen}s: %s", "Locked status", $locked_status);
my $shortlist_status = get_shortlist_status();
#print "\nShortlisted: " . get_shortlist_status();
printf("\n%-${headingLen}s: %s", "Shortlisted", $shortlist_status);
my @cids = uniq get_child_branches_by_id(@bid);
my @child_name = ();
if (scalar @cids !=0) {
  for my $cid (@cids){
    push(@child_name, get_branch_name_by_branch_id($cid));
  }
  @child_name = uniq @child_name;
  #print "\n\nChild branches: @child_name";
  printf("\n%-${headingLen}s: %s, @child_name", "Child branches", scalar @child_name);
}
else {
  #print "\n\nChild branches: ...";
  printf("\n%-${headingLen}s: %s", "Child branches", "No Child");
}
my @sha_id = uniq get_sha_id_by_branch_id(@bid);
if ( scalar @sha_id == 0 ) {
  printf("\n\n%-${headingLen}s: %s", "SHA of last few commits", "No SHA");
}
else {
  printf("\n\n%-${headingLen}s: @sha_id", "SHA of last few commits");
}
print "\n\nSync/Merge information: ..\n\n";
} # print_result_detail

# --------------------- print_result_timestamp
sub print_result_timestamp{
  my $utcTime = $result->{build_time};
  my $displayDT = get_displayDT($utcTime);
  printf("%s  ", $result->{release});
  printf("%s\n", $displayDT);
} # print_result_timestamp

# ------------ printDebug
sub printDebug {
  my $msg = shift;
  print "$msg\n" if ($debug) ;
} #printDebug

#----------getParent

sub get_parent_id {
  my $branch_name = shift;
  my @parent_id = ();
  my @data = ();
  my $sql = qq {
     SELECT parent_id FROM vcs.branch_parent
     JOIN vcs.branch USING (branch_id)
     WHERE branch_name = ?
  };
  my $sth = $dbh->prepare($sql);
  $sth->execute( $branch_name);
  while ( @data = $sth->fetchrow_array() ) {
      push (@parent_id, $data[0]);
          }
  return @parent_id;
}


sub get_branch_name_by_branch_id {
    # my $branch_name = shift;
  my $branch_id = shift;
  my @branch_name = ();
  my @data = ();
  my $sql = qq {
    SELECT branch_name FROM vcs.branch WHERE branch_id = ?
  };
  my $sth = $dbh->prepare($sql);
  $sth->execute($branch_id);
  while ( @data = $sth->fetchrow_array() ) {
    push (@branch_name, $data[0]);
  }
  return @branch_name;
}

sub get_created_ts{
    # my $branch_name = shift;
  my $branch_id = shift;
  my @created_ts = ();
  my @data = ();
  my $sql = qq {
    SELECT created_ts FROM vcs.branch WHERE branch_id = ?
  };
  my $sth = $dbh->prepare($sql);
  $sth->execute($branch_id);
  while ( @data = $sth->fetchrow_array() ) {
    push (@created_ts, $data[0]);
  }
  return @created_ts;
}


sub get_pull_sha{
    # my $branch_name = shift;
  my $branch_id = shift;
  my @pull_sha = ();
  my @data = ();
  my $sql = qq {
    SELECT pull_sha FROM vcs.branch WHERE branch_id = ?
  };
  my $sth = $dbh->prepare($sql);
  $sth->execute($branch_id);
  while ( @data = $sth->fetchrow_array() ) {
    push (@pull_sha, $data[0]);
  }
  return @pull_sha;
}


sub get_bdrelease_by_time {
  #my $branch_id = shift;
  my $ts = shift;
  my @branch_ids = @_;
  my @bdrelease = ();
  my @data = ();
  foreach my $branch_id (@branch_ids){
  my $sql = qq {
   SELECT  bd.release, bd.branch_id
   FROM public.build bd
   WHERE branch_id = ?
   AND bd.build_time = ?
   };
  my $sth = $dbh->prepare($sql);
  $sth->execute($branch_id,$ts);
  while ( @data = $sth->fetchrow_array() ) {
      #print "\n\nData: @data";
    push (@bdrelease, @data);
  }
  }
  return @bdrelease;
}

sub get_branch_type{
    # my $branch_name = shift;
  my $branch_id = shift;
  my @branch_type = ();
  my @data = ();
  my $sql = qq {
    SELECT branch_type FROM vcs.branch WHERE branch_id = ?
  };
  my $sth = $dbh->prepare($sql);
  $sth->execute($branch_id);
  while ( @data = $sth->fetchrow_array() ) {
    push (@branch_type, $data[0]);
  }
  return @branch_type;
}


sub get_branch_status{
    # my $branch_name = shift;
  my $branch_id = shift;
  my @branch_status = ();
  my @data = ();
  my $sql = qq {
    SELECT branch_status FROM vcs.branch WHERE branch_id = ?
  };
  my $sth = $dbh->prepare($sql);
  $sth->execute($branch_id);
  while ( @data = $sth->fetchrow_array() ) {
    push (@branch_status, $data[0]);
  }
  return @branch_status;
}

#----------------------getShortlistStatus

sub get_shortlist_status{
  my @repo = split('\.',$repo_name);
  my $branch_repo = $branch_name . "-" . $repo[0] ;
  my $output  = `shortlist show $branch_repo`;
  my @output_list = split('\n',$output);
  my $output_len = @output_list;
  if ( $output_len == 1 ){
    return $output;
  }
  else {
    return "Tree \'$branch_repo\' has shortlist.\n";
  }
}

#-----------------------getChildBranches

sub get_child_branches_by_id {
  my @ids = @_;
  my @child_ids = ();
  my @data = ();
  foreach my $id (@ids) {
     my $sql = qq {
     SELECT branch_id
     FROM   vcs.branch_parent
     WHERE parent_id = ?
     };
     my $sth = $dbh->prepare($sql);
     $sth->execute($id);
    while ( @data = $sth->fetchrow_array() ) {
      push (@child_ids, $data[0]);
    }
  }
  return @child_ids;
}

#--------------------getSHAid

sub get_sha_id_by_branch_id {
  my @ids = @_;
  my @sha_ids = ();
  my @data = ();
  foreach my $id (@ids){
  my $sql = qq {
   SELECT sha
   FROM   public.build
   WHERE branch_id = ?
   AND "sha" is NOT null
   LIMIT 5
   };
  my $sth = $dbh->prepare($sql);
  $sth->execute($id);
  while ( @data = $sth->fetchrow_array() ) {
      #print "\n\nData: @data \n";
    push (@sha_ids, $data[0]);
  }
  }
  return @sha_ids;
}


