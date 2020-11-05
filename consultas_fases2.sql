use cuentas;
SELECT * FROM banco;
SELECT * FROM(
SELECT YEAR(s.fecha) AS ano, MONTH(s.fecha) AS mes, b.nombre_banco, SUM(saldo) AS saldo, RANK() OVER (PARTITION BY YEAR(s.fecha), MONTH(s.fecha) ORDER BY SUM(saldo) DESC) ranker
FROM banco b
JOIN saldo s
ON b.id_banco = s.id_banco
WHERE s.tipo = 'A' 
GROUP BY YEAR(s.fecha), MONTH(s.fecha), b.nombre_banco) AS temp
WHERE temp.nombre_banco = 'DE CRÉDITO, S. A.';

select * from saldo;
INSERT INTO saldo (fecha,id_banco,tipo,saldo) VALUES ('2019-11-30',6,'A',0);
INSERT INTO saldo (fecha,id_banco,tipo,saldo) VALUES ('2020-06-30',6,'A',0);
INSERT INTO saldo (fecha,id_banco,tipo,saldo) VALUES ('2020-07-31',6,'A',0);
