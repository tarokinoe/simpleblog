import psycopg2
from project import settings
from blogapp.db import TAG_MAX_LENGTH


conn = psycopg2.connect(**settings.DB)
cursor = conn.cursor()


cursor.execute(
    """
    CREATE EXTENSION IF NOT EXISTS pg_trgm;
    DROP TABLE IF EXISTS public.posts;
    DROP SEQUENCE IF EXISTS public.posts_id_seq;
    DROP TABLE IF EXISTS public.users;
    DROP SEQUENCE IF EXISTS public.users_id_seq ;
        
    CREATE SEQUENCE public.users_id_seq
      INCREMENT 1
      MINVALUE 1
      MAXVALUE 9223372036854775807
      START 1
      CACHE 1;
    
    CREATE TABLE public.users (
      id int NOT NULL DEFAULT nextval('users_id_seq'::regclass),
      username varchar(30) NOT NULL,
      CONSTRAINT user_pkey PRIMARY KEY (id)
    );
    
    CREATE SEQUENCE posts_id_seq
      INCREMENT 1
      MINVALUE 1
      MAXVALUE 9223372036854775807
      START 1
      CACHE 1;
    
    CREATE TABLE public.posts (
        id int NOT NULL DEFAULT nextval('posts_id_seq'::regclass),
        title varchar(255) NOT NULL,
        text varchar(255) NOT NULL,
        author_id int NOT NULL,
        date_created timestamptz NOT NULL,
        tags varchar({tag_max_length})[],
        CONSTRAINT posts_pkey PRIMARY KEY (id),
        CONSTRAINT posts_author_id_fk_user_id FOREIGN KEY (author_id)
          REFERENCES public.users (id) MATCH SIMPLE
          ON UPDATE NO ACTION ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED
    );
    DROP INDEX IF EXISTS posts_tags; 
    CREATE INDEX posts_tags ON public.posts USING gin (tags);
    DROP INDEX IF EXISTS posts_date_created; 
    CREATE INDEX posts_date_created ON public.posts USING btree (date_created);
    DROP INDEX IF EXISTS trgm_idx_posts_title;
    CREATE INDEX trgm_idx_posts_title ON public.posts USING gin (title gin_trgm_ops);
    """.format(
        tag_max_length=TAG_MAX_LENGTH
    )
)

conn.commit()
cursor.close()
conn.close()
