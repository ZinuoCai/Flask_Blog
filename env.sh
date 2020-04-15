source activate flask_env
export SECRET_KEY=dc8e08a07a2540c336b11dde71de8853
export SQLALCHEMY_DATABASE_URI=sqlite:///site.db
export EMAIL_USER=zinuocai@gmail.com
export EMAIL_PASS=tlrxzwjfwzzkeaes
nohup python run.py > log &
