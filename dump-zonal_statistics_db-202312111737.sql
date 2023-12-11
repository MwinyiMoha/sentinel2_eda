--
-- PostgreSQL database dump
--

-- Dumped from database version 13.4 (Debian 13.4-4.pgdg110+1)
-- Dumped by pg_dump version 14.9 (Ubuntu 14.9-1.pgdg20.04+1)

-- Started on 2023-12-11 17:37:03 EAT

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

--
-- TOC entry 2994 (class 1262 OID 296213)
-- Name: zonal_statistics_db; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE zonal_statistics_db WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'en_US.utf8';


ALTER DATABASE zonal_statistics_db OWNER TO postgres;

\connect zonal_statistics_db

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

--
-- TOC entry 3 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO postgres;

--
-- TOC entry 2995 (class 0 OID 0)
-- Dependencies: 3
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 201 (class 1259 OID 296227)
-- Name: test_roi_tbl; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.test_roi_tbl (
    id integer NOT NULL,
    image_date character varying,
    min double precision,
    max double precision,
    mean double precision,
    median double precision,
    std_dev double precision
);


ALTER TABLE public.test_roi_tbl OWNER TO postgres;

--
-- TOC entry 200 (class 1259 OID 296225)
-- Name: test_roi_tbl_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.test_roi_tbl_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.test_roi_tbl_id_seq OWNER TO postgres;

--
-- TOC entry 2996 (class 0 OID 0)
-- Dependencies: 200
-- Name: test_roi_tbl_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.test_roi_tbl_id_seq OWNED BY public.test_roi_tbl.id;


--
-- TOC entry 2854 (class 2604 OID 296230)
-- Name: test_roi_tbl id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.test_roi_tbl ALTER COLUMN id SET DEFAULT nextval('public.test_roi_tbl_id_seq'::regclass);


--
-- TOC entry 2988 (class 0 OID 296227)
-- Dependencies: 201
-- Data for Name: test_roi_tbl; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.test_roi_tbl VALUES (1, '20221127T075159', -0.09801489114761353, 0.6830308437347412, 0.4559508058515745, 0.473158061504364, 0.08535949040619054);


--
-- TOC entry 2997 (class 0 OID 0)
-- Dependencies: 200
-- Name: test_roi_tbl_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.test_roi_tbl_id_seq', 1, true);


--
-- TOC entry 2856 (class 2606 OID 296235)
-- Name: test_roi_tbl test_roi_tbl_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.test_roi_tbl
    ADD CONSTRAINT test_roi_tbl_pkey PRIMARY KEY (id);


-- Completed on 2023-12-11 17:37:03 EAT

--
-- PostgreSQL database dump complete
--

