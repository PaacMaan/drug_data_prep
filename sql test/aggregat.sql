-- Create PRODUCT_NOMENCLATURE table
create table PRODUCT_NOMENCLATURE(product_id integer, product_type varchar(100), product_name varchar(100));
insert into PRODUCT_NOMENCLATURE(product_id, product_type, product_name) values(490756, "MEUBLE", "Chaise");
insert into PRODUCT_NOMENCLATURE(product_id, product_type, product_name) values(389728, "DECO", "Boule de Noël");
insert into PRODUCT_NOMENCLATURE(product_id, product_type, product_name) values(549380, "MEUBLE", "Canapé");
insert into PRODUCT_NOMENCLATURE(product_id, product_type, product_name) values(293718, "DECO", "Mug");

-- Create Transactions table

CREATE table TRANSACTION(daate varchar(100), order_id integer, client_id integer, prop_id integer, prod_price integer, prod_qty integer);
insert into TRANSACTION values("01/01/20", 1234, 999, 490756, 50, 1);
insert into TRANSACTION values("01/01/20", 1234, 999, 389728, 3.56, 4);
insert into TRANSACTION values("01/01/20", 3456, 845, 490756, 50, 2);
insert into TRANSACTION values("01/01/20", 3456, 845, 549380, 300, 1);
insert into TRANSACTION values("01/01/20", 3456, 845, 293718, 10, 6);


-- First Question's Answer
SELECT date, SUM(prod_price * prod_qty) AS "ventes"
FROM TRANSACTION 
GROUP BY date 
ORDER BY date ASC;



-- second question's answer
SELECT client_id,
       sum(CASE WHEN pn.product_type = 'MEUBLE' THEN prod_price * prod_qty END) AS ventes_meubles,
       sum(CASE WHEN pn.product_type = 'DECO' THEN prod_price * prod_qty END) AS ventes_decp
FROM TRANSACTION t JOIN
     PRODUCT_NOMENCLATURE pn
     ON t.prop_id = pn.product_id
GROUP BY client_id
