from environs import Env

env = Env()
env.read_env()

TOKEN = env.str("TOKEN")
PGUSER = env.str("PGUSER")
PGPASSWORD = env.str("PGPASSWORD")
PGHOST = env.str("PGHOST")
PGDATABASE = env.str("PGDATABASE")
SUPERUSER = env.str("SU")

POSTGRES_URI = f"postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}/{PGDATABASE}"
