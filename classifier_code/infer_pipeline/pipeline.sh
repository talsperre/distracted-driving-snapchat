#!/bin/bash
#SBATCH -n 40
#SBATCH --mem-per-cpu=2048
#SBATCH --time=72:00:00
#SBATCH --mincpus=40
#SBATCH --mail-user=dheerajreddy.p@students.iiit.ac.in
#SBATCH --mail-type=ALL
#SBATCH -A dheerajreddy.p
#SBATCH --gres=gpu:1

module add cuda/8.0
module add cudnn/7-cuda-8.0

# USAGE - sbatch ~/infer_pipeline/pipeline.sh <ID> <dd_mm_yyyy> <scratch_dir>
# EXAMPLE - sbatch ~/infer_pipeline/pipeline.sh 1rdswoJ0O5Z2jT2Dr9wcV8tetGpvixcL3 15_03_2019 /scratch/dheeraj 8081

# $1 - ID
# #2 - date in format dd_mm_yyy
# $3 - scratch dir
# $4 - port for jupyter

#source /home/dheerajreddy.p/fenv/bin/activate

bash /home/dheerajreddy.p/jp.sh $4 $4 10.1.39.79 dheeraj

node=$(hostname)

curl -X POST -H ‘Content-type: application/json’ --data '{"text":"Beginning inference pipeline for '$2' on '$USER'@'$node'"}' https://hooks.slack.com/services/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

#curl -X POST -H 'Content-type: application/json' --data '{"text":"<@UCMBT0N5V> <@UCEKSNSJE> Checking for missing videos encountered an error!"}' https://hooks.slack.com/services/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

# Setting default GPU to 0
#export CUDA_VISIBLE_DEVICES=0

echo "Activating virtualenv"
source /home/dheerajreddy.p/fenv/bin/activate

# Deleting scratch dir if it already exists
# rm -rf $3

# Name of tar file being downloaded
tar_name="$2.tar"

# Creating blank directory in scratch if it doesn't already exist
mkdir $3

# Download and extract tar file
curl -X POST -H ‘Content-type: application/json’ --data '{"text":"Downloading tar file for '$2' on '$USER'@'$node'"}' https://hooks.slack.com/services/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
python ~/infer_pipeline/download.py $1 $3 $tar_name
if [ $? -eq 0 ]; then
    echo OK
else
    curl -X POST -H ‘Content-type: application/json’ --data '{"text":"<@UCMBT0N5V> <@UCEKSNSJE> FAILED Downloading tar file for '$2' on '$USER'@'$node'"}' https://hooks.slack.com/services/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
    exit
fi
file_dir="$3/$tar_name"

# Extracting tar file
cd $3
video_dir="$3/video"
new_video_dir="$video_dir$2"
curl -X POST -H ‘Content-type: application/json’ --data '{"text":"Extracting tar file for '$2' on '$USER'@'$node'"}' https://hooks.slack.com/services/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
tar -xf $file_dir 
if [ $? -eq 0 ]; then
    rm -rf $file_dir
    mv $video_dir $new_video_dir
else
    curl -X POST -H ‘Content-type: application/json’ --data '{"text":"<@UCMBT0N5V> <@UCEKSNSJE> FAILED to untar file for '$2' on '$USER'@'$node'"}' https://hooks.slack.com/services/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
    exit
fi
# video directory is created after extraction - /scratch/dheeraj/videodd_mm_yyyy - this directory consists of all the videos needed to classify


frame_dir="$3/frames$2"
csv_dir="$HOME/infer_pipeline/csvs/$2.csv"

curl -X POST -H ‘Content-type: application/json’ --data '{"text":"Converting videos to frames for '$2' on '$USER'@'$node'"}' https://hooks.slack.com/services/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
python ~/infer_pipeline/frame_split.py --video_dir $new_video_dir --dest_dir $frame_dir --metadata_csv $csv_dir
if [ $? -eq 0 ]; then
    rm -rf $new_video_dir
else
    curl -X POST -H ‘Content-type: application/json’ --data '{"text":"<@UCMBT0N5V> <@UCEKSNSJE> FAILED to convert video to frames for '$2' on '$USER'@'$node'"}' https://hooks.slack.com/services/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
    exit
fi


curl -X POST -H ‘Content-type: application/json’ --data '{"text":"Classifying frames for '$2' on '$USER'@'$node'. Trying GPU 0."}' https://hooks.slack.com/services/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
pred_file="$HOME/$2_pred.csv"
python ~/infer_pipeline/image_classifier.py --save_file $pred_file --frame_dir $frame_dir
if [ $? -eq 0 ]; then
    echo OK
    rm -rf $frame_dir
else
#    curl -X POST -H ‘Content-type: application/json’ --data '{"text":"Converting videos to frames for '$2' on '$USER'@'$node'. Trying GPU 1."}' https://hooks.slack.com/services/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
#    export CUDA_VISIBLE_DEVICES=1
#    python ~/infer_pipeline/image_classifier.py --save_file $pred_file --frame_dir $frame_dir
#    if [ $? -eq 0 ]; then
#        echo OK
#        rm -rf $frame_dir
#    else
#        curl -X POST -H ‘Content-type: application/json’ --data '{"text":"Classifying frames for '$2' on '$USER'@'$node'. Trying GPU 2."}' https://hooks.slack.com/services/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
#        export CUDA_VISIBLE_DEVICES=2
#        python ~/infer_pipeline/image_classifier.py --save_file $pred_file --frame_dir $frame_dir
#        if [ $? -eq 0 ]; then
#            echo OK
#            rm -rf $frame_dir
#        else
#            curl -X POST -H ‘Content-type: application/json’ --data '{"text":"Classifying frames for '$2' on '$USER'@'$node'. Trying GPU 3."}' https://hooks.slack.com/services/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
#            export CUDA_VISIBLE_DEVICES=3
#            python ~/infer_pipeline/image_classifier.py --save_file $pred_file --frame_dir $frame_dir
#            if [ $? -eq 0 ]; then
#                echo OK
#                rm -rf $frame_dir
#            else
#                curl -X POST -H ‘Content-type: application/json’ --data '{"text":"<@UCMBT0N5V> <@UCEKSNSJE> FAILED to classify frames for '$2' on '$USER'@'$node'"}' https://hooks.slack.com/services/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
#                exit
#            fi
#        fi
#    fi
    curl -X POST -H ‘Content-type: application/json’ --data '{"text":"<@UCMBT0N5V> <@UCEKSNSJE> Classification FAILED for '$2' on '$USER'@'$node'."}' https://hooks.slack.com/services/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
fi

curl -X POST -H ‘Content-type: application/json’ --data '{"text":"Successfully completed inference pipeline for '$2' on '$USER'@'$node'"}' https://hooks.slack.com/services/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
