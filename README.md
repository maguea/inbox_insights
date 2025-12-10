# Inbox Insight
## Getting started
NOTE: you may need the python extension
1. if you have not, create the venv with "Python: Create Environment"
2. start the virtual environment
3. install flask with `pip install -r requirements.txt`

## options to run
1. run `python -m src.app` in terminal from `/` 
2. `ctrl+shift+p` and search for "Debug: Start Without Debugging". you can also press `ctrl+F5`
3. in the status bar, you can see "Run app.py (inbox_insights)" and can click on that to run. You can do this, but i prefer not to since it wont update html i work on and if you make changes to any py script while `debug=True` in [app.py](/src/app.py) you have to hot reload instead of it automatically reloading the service for you.
   
## view web page
you should see the IP:PORT in the terminal when you run the app. you can ctrl+click on it and it should take you to the browser.

currently: [localhost:5000](http://localhost:5000)

## Database
### .env
fill in these values into the `.env`

```
PG_DB=
PG_USER=
PG_PASS=
PG_HOST=
PG_PORT=
```
### table creation
create the two necessary tables like so
```sql
CREATE TABLE IF NOT EXISTS public.email_data
(
    id integer NOT NULL DEFAULT nextval('email_data_id_seq'::regclass),
    user_id character varying(70) COLLATE pg_catalog."default",
    sender_add jsonb DEFAULT '{}'::jsonb,
    category character varying(20) COLLATE pg_catalog."default",
    data jsonb,
    collected_date timestamp without time zone NOT NULL DEFAULT now(),
    delete_date timestamp without time zone,
    CONSTRAINT email_data_pkey PRIMARY KEY (id)
)
```
and
```sql
CREATE TABLE IF NOT EXISTS public.user_data
(
    user_id text COLLATE pg_catalog."default" NOT NULL,
    user_pass character varying(50) COLLATE pg_catalog."default" NOT NULL,
    user_key character varying(50) COLLATE pg_catalog."default",
    priv_cats jsonb DEFAULT '[]'::jsonb,
    CONSTRAINT user_data_pkey PRIMARY KEY (user_id)
)
```
