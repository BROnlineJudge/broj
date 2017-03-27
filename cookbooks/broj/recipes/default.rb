# Update
# execute 'add-apt-repository -y ppa:ubuntu-toolchain-r/test'
# execute 'add-apt-repository ppa:fkrull/deadsnakes'
# execute 'apt-get update'

# GCC / G++
package 'gcc-6'
execute 'update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-6 90'
package 'g++-6'
execute 'update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-6 90'

# Python 3.6
package 'python3.6'
package 'python3-pip'
execute 'pip3 install virtualenv'

# PostgreSQL
package 'libpq-dev'
package 'postgresql'
service 'postgresql' do
  action [:restart, :enable]
end
execute "create broj user" do
  command "psql -c \"CREATE USER broj WITH PASSWORD 'password';\""
  user "postgres"
  action :run
  not_if "psql postgres -tAc \"SELECT 1 FROM pg_roles WHERE rolname='broj'\" | grep -q 1"
end
execute "createdb -O broj broj_dev" do
  user "postgres"
  action :run
  not_if 'psql -lqt | cut -d \| -f 1 | grep -qw broj_dev'
end

# BROJ config file
execute 'mkdir -p /opt/broj'
execute 'chown vagrant -R /opt/broj'
template '/opt/broj/config.ini' do
  source 'config.erb'
  owner 'vagrant'
  not_if 'ls /opt/broj/ | grep -q "config.ini"'
end

# virtualenv
execute 'echo "cd /vagrant_data/" >> /home/vagrant/.bashrc'
execute 'create venv' do
  user 'vagrant'
  command 'virtualenv -p /usr/bin/python3.6 /home/vagrant/.virtualenvs/broj_venv'
  not_if 'ls /home/vagrant/.virtualenvs | grep -q "broj_venv"'
end
execute 'auto enter venv' do
  command 'echo "source /home/vagrant/.virtualenvs/broj_venv/bin/activate" >> /home/vagrant/.bashrc'
  not_if 'cat /home/vagrant/.bashrc | grep -q "source /home/vagrant/.virtualenvs/broj_venv/bin/activate"'
end

# execute 'pip3 install -r /vagrant_data/requirements.txt'
