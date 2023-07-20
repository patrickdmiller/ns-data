docker run  --ipc=host --gpus all  -it --rm -p 8888:8888 -v $PWD:/py/ ns-data bash -c "cd /py/ && jupyter notebook --allow-root --ip 0.0.0.0 --port 8888 --no-browser --NotebookApp.allow_origin='*' --NotebookApp.token='password'"

