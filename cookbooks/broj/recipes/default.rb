# execute 'add-apt-repository -y ppa:ubuntu-toolchain-r/test'
# execute 'add-apt-repository ppa:fkrull/deadsnakes'
# execute 'apt-get update'

# package 'gcc-6'
# execute 'update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-6 90'
# package 'g++-6'
# execute 'update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-6 90'

# package 'python3.6'
# package 'python3-pip'

package 'libpq-dev'
execute 'pip3 install -r /vagrant_data/requirements.txt'
