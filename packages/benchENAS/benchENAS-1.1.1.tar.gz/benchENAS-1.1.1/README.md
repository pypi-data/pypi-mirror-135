- The codes have been tested on Python 3.6 + pytorch 1.1 + torchvision 0.3.0 (pytorch 1.3 seems also ok, but not test thoroughly)

- BenchENAS is a platform to help researchers conduct fair comparisons upon Evolutionary algorithm based Neural Architecture Search (ENAS) algorithms. BenchENAS currently has the following features (more are still in process, and welcome join us to contribute BenchENAS):
 -  Nine representative state-of-the-art ENAS algorithms have been implemented into BenchENAS. They can be easily performed with customized benchmark datasets (including popular preprocessing techniques) and training algorithms (such as learning rate, optimizers, etc).

 - A GPU distributed training component is designed in BenchENAS to accelerate fitness evaluation. This component is specifically developed for common research environments where not many GPUs are specifically prepared.

 - BenchENAS is implemented by native Python with very few third-party libraries for easy installation. All components in BenchENAS can be easily configured with different data settings and different trainer settings.

 - BenchENAS is modular designed for easy extensibility. Researchers can easily implement their ENAS algorithms into BenchENAS, while directly using the implemented datasets, training algorithms (can also add their own datasets and training algorithms into BenchENAS), and distributed training components.
- A research paper comprehensively introducing BenchENAS is available at: https://arxiv.org/abs/2108.03856.

- #Requirements:

 - Center Computer:
   - redis (ubuntu software, start using the command redis-server --protected-mode on)
   - sshpass (python lib)

 - Conter Computer & workers:
   - multiprocess (python lib)
   - redis (python lib)
 
- #Parameter
- alg_list = {'algorithm': 'cnn_ga', 'max_gen': 20, 'pop_size': 30, 'log_server': '192.XX.XX.XX', 'log_server_port': 6379, 'exe_path': '/home/XX/anaconda3/bin/python3'}

- train_list = {'dataset': 'CIFAR10', 'optimizer': 'SGD', 'lr': 0.025, 'batch_size': 64, 'total_epoch': 50, 'lr_strategy': 'ExponentialLR'}

- gpu_info_list = {}
- content = {'worker_ip': '192.XX.XX.XX', 'worker_name': 'cuda', 'ssh_name': 'XX', 'ssh_password': 'XXXXXX', 'gpu': [0, 1]}
- gpu_info_list['192.168.50.202'] = content

- #How to use
- Start the redis-server on the center computer (redis-server --protected-mode no)
- Start the init_compute.py script to start the compute platform with parameter[run(alg_list,  train_list,  gpu_info_list)]
- Start the algorithm you would like to perform with parameter[run(alg_list,  train_list,  gpu_info_list, search_space)] search_space default 'micro' 