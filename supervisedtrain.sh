export CUDA_VISIBLE_DEVICES=1,2,3,4

python ./main.py \
      --todo supervisedtrain \
      --save_folder 50play\
      --n_train_data 5\
      --load_data_folder stable_10_10_5\
      --trainepochs 500