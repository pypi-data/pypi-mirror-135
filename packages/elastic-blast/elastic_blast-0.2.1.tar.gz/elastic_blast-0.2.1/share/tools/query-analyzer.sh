#!/bin/bash
# query-analyzer.sh: Split the query sequence provided and print a summary of
# the data generated
#
# Author: Christiam Camacho (camacho@ncbi.nlm.nih.gov)
# Created: Fri 30 Jul 2021 02:16:05 PM EDT

query=${1:-s3://elasticblast-test/queries/GCA_018506945.1_HG005.alt.pat.f1_v2_genomic.fna.gz}
batch_len=${2:-5000000}

qlen=`mktemp`
output_dir=`mktemp -d`
tmp_dir=`mktemp -d`
single_fasta=`mktemp -t $(basename -s .sh $0)-XXXXXXX.fa`
SCRIPT_DIR=$(cd "`dirname "$0"`"; pwd)
trap " /bin/rm -fr $single_fasta $tmp_dir $output_dir $qlen " INT QUIT EXIT HUP KILL ALRM

if [[ $query =~ ".query-list" ]]; then
    echo "Processing .query-list file"
    if [[ $query =~ "s3://" ]]; then
        aws s3 cp --only-show-errors $query - | parallel aws s3 cp --only-show-errors {} $output_dir/
    else
        gsutil -qm cat $query | parallel gsutil -qm cp {} $output_dir/
    fi
    parallel gunzip {} ::: $output_dir/*.gz
    cat $output_dir/* > $single_fasta
    query=$single_fasta
fi

$SCRIPT_DIR/../../bin/fasta_split.py -l $batch_len -o $output_dir -c $qlen $query

printf "Query file: %s\n" $query
printf "Query length: %'d\n" `cat $qlen`
printf "Batch length: %'d\n" $batch_len
printf "Number of batches: %'d\n" `ls -1 $output_dir/*.fa| wc -l`

for f in $output_dir/*.fa; do
    num_seqs=`grep -c '^>' $f`
    query_batch_length=`grep -v '^>' $f | tr '\n' ' ' | tr -d ' ' | wc -c`
    printf "%-20s %'10d seqs %'10d letters\n" `basename $f` $num_seqs $query_batch_length
done
