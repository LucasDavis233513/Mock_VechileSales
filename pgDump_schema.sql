--
-- PostgreSQL database dump
--

-- Dumped from database version 16.2 (Postgres.app)
-- Dumped by pg_dump version 16.2 (Postgres.app)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: cars; Type: TABLE; Schema: public; Owner: lucasdavis
--

CREATE TABLE public.cars (
    car_id integer NOT NULL,
    make character varying(25),
    model character varying(50),
    year integer,
    selling_price double precision,
    seller_id integer NOT NULL,
    detail_id integer NOT NULL
);


ALTER TABLE public.cars OWNER TO lucasdavis;

--
-- Name: details; Type: TABLE; Schema: public; Owner: lucasdavis
--

CREATE TABLE public.details (
    detail_id integer NOT NULL,
    transmission character varying(10),
    color character varying(10),
    interior_color character varying(10),
    body character varying(25),
    "trim" character varying(255),
    condition integer,
    odometer integer,
    vin character varying(255),
    mmr double precision
);


ALTER TABLE public.details OWNER TO lucasdavis;

--
-- Name: purchases; Type: TABLE; Schema: public; Owner: lucasdavis
--

CREATE TABLE public.purchases (
    purchase_id integer NOT NULL,
    user_id integer NOT NULL,
    car_id integer NOT NULL,
    date date
);


ALTER TABLE public.purchases OWNER TO lucasdavis;

--
-- Name: seller; Type: TABLE; Schema: public; Owner: lucasdavis
--

CREATE TABLE public.seller (
    seller_id integer NOT NULL,
    name character varying(255),
    state character varying(255)
);


ALTER TABLE public.seller OWNER TO lucasdavis;

--
-- Name: users; Type: TABLE; Schema: public; Owner: lucasdavis
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    username character varying(255),
    password character varying(255),
    email character varying(50),
    city character varying(255),
    state character varying(255),
    zip_code character varying(255),
    active boolean
);


ALTER TABLE public.users OWNER TO lucasdavis;

--
-- Name: cars cars_pkey; Type: CONSTRAINT; Schema: public; Owner: lucasdavis
--

ALTER TABLE ONLY public.cars
    ADD CONSTRAINT cars_pkey PRIMARY KEY (car_id);


--
-- Name: details details_pkey; Type: CONSTRAINT; Schema: public; Owner: lucasdavis
--

ALTER TABLE ONLY public.details
    ADD CONSTRAINT details_pkey PRIMARY KEY (detail_id);


--
-- Name: purchases purchases_pkey; Type: CONSTRAINT; Schema: public; Owner: lucasdavis
--

ALTER TABLE ONLY public.purchases
    ADD CONSTRAINT purchases_pkey PRIMARY KEY (purchase_id);


--
-- Name: seller seller_pkey; Type: CONSTRAINT; Schema: public; Owner: lucasdavis
--

ALTER TABLE ONLY public.seller
    ADD CONSTRAINT seller_pkey PRIMARY KEY (seller_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: lucasdavis
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: cars cars_detail_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: lucasdavis
--

ALTER TABLE ONLY public.cars
    ADD CONSTRAINT cars_detail_id_fkey FOREIGN KEY (detail_id) REFERENCES public.details(detail_id);


--
-- Name: cars cars_seller_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: lucasdavis
--

ALTER TABLE ONLY public.cars
    ADD CONSTRAINT cars_seller_id_fkey FOREIGN KEY (seller_id) REFERENCES public.seller(seller_id);


--
-- Name: purchases purchases_car_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: lucasdavis
--

ALTER TABLE ONLY public.purchases
    ADD CONSTRAINT purchases_car_id_fkey FOREIGN KEY (car_id) REFERENCES public.cars(car_id);


--
-- Name: purchases purchases_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: lucasdavis
--

ALTER TABLE ONLY public.purchases
    ADD CONSTRAINT purchases_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- PostgreSQL database dump complete
--

