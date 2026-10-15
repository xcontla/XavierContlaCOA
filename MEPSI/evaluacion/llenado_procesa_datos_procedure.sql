DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `forSPSS`(id_usuario bigint, OUT out_number varchar(512))
BEGIN
  DECLARE done INT DEFAULT FALSE;
  DECLARE d varchar(128);
  DECLARE s varchar(512);
  DECLARE a, b , c INT;
  DECLARE cur1 CURSOR FOR select e.id_usuario, e.id_usuario_examen, e.id_examen, r.c_respuesta from usuario_examen e
inner join usuario_respuesta r on r.id_usuario_examen = e.id_usuario_examen
where e.id_usuario = id_usuario order by id_examen;
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

  OPEN cur1;

    set s = '';
  read_loop: LOOP
    FETCH cur1 INTO a, b, c, d;
   
    IF done THEN
      LEAVE read_loop;
    END IF;
 IF c = 1 THEN
        set s =  CONCAT(s,d);
      END IF;
      IF c = 2 THEN
set s =  CONCAT(s,d,'                                             ');
      END IF;
      IF c = 3 THEN
  set s = CONCAT(s,d,'      ');    
      END IF;      
      IF c = 4 THEN
  set s = CONCAT(s,d,' ');      
      END IF;      
      IF c = 5 THEN
  set s = CONCAT(s,d,'     ');      
      END IF;      
      IF c = 6 THEN
  set s = CONCAT(s,d,'       ');      
      END IF;      
      IF c = 7 THEN
  set s = CONCAT(s,d,'   ');      
      END IF;
      IF c = 8 THEN
  set s = CONCAT(s,d);
       end if;
     
  END LOOP;

  CLOSE cur1;
 
SET out_number = s;
END$$
DELIMITER ;
DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `generarResultado`()
BEGIN  
  DECLARE done2 INT DEFAULT FALSE;
  DECLARE id, total INT;
  DECLARE paterno, materno, nombres, sexo, num_cuenta, posgrado, nivel varchar(255);
  DECLARE respuestas varchar(512);
 
  DECLARE cur CURSOR FOR select uda.id_usuario, uda.c_apPaterno, uda.c_apMaterno, uda.c_nombres,  uda.c_sexo, uda.c_num_cuenta,
uda.c_posgrado_ingresar, uda.c_nivel, count(ue.id_examen) as t from usuario_examen ue
inner join usuario_datos_alumno uda on uda.id_usuario = ue.id_usuario
                            where uda.id_usuario in
                            (
								23769, 28589, 28592, 26131, 28595, 28594, 28599, 26179, 28588, 27818, 26311, 28610, 26201, 28607, 28617, 28642, 28619, 28633, 28632, 28596, 
                                28627, 28572, 28624, 28629, 20853, 26148, 26168, 28221, 28643, 26172, 28652, 28657, 28659, 28661, 21775, 26198, 28669, 17050, 19092, 19142, 
                                15588, 15585, 15587, 17069, 17012, 26530, 28682, 17023, 17022, 11530, 17072, 15573, 20844, 17046, 15564, 11526, 6715, 17035, 
                                
                                26536, 12679, 26528, 31197, 15507, 18256, 28418, 26535, 26546, 28587, 21672, 2600, 26551, 12779, 9789, 28582, 18136, 12836, 12848, 18153, 
                                17993, 27030, 28388, 9447, 12955, 17802, 19318, 18017, 22631, 17937, 
                                
                                15489, 28912, 9971, 13209, 9961, 26227, 15442, 17426, 13238, 10006, 15474, 28905, 26251, 28909, 9967, 21684, 1901, 28911, 7728, 28939, 21705, 
                                23521, 27587, 28934, 27797, 28922, 28941, 28918, 8199, 17678, 26245, 26250, 28919, 26258, 26259, 21712, 13285, 27412, 19729, 13905, 13917, 13919, 
                                28954, 26271, 23570, 28955, 28946, 28947, 28965, 26281, 28958, 19717, 19718, 28960, 23174, 
                                
                                30255, 29789, 14814
                            )
                           
                             or uda.id_usuario between 31123 and 31212 or uda.id_usuario between 31247 and 31384
                           
                            group by uda.id_usuario;
                           
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done2 = TRUE;
 
  set respuestas = '';
 
  OPEN cur;
  read_loop: LOOP
FETCH cur INTO id, paterno, materno, nombres, sexo, num_cuenta, posgrado, nivel, total;
    IF done2 THEN
      LEAVE read_loop;
    END IF;
   
   
   
    if total = 8 then
   
call forSPSS(id,@out_value);
   
     
    -- select  @out_value;

CREATE TABLE if not EXISTS `usuario_procesa_datos` (
  `id_usuario` int(11) NOT NULL,
  `c_apPaterno` varchar(255) NOT NULL,
  `c_apMaterno` varchar(255) DEFAULT NULL,
  `c_nombres` varchar(255) DEFAULT NULL,
  `c_sexo` varchar(255) DEFAULT NULL,
  `c_num_cuenta` varchar(255) DEFAULT NULL,
  `c_posgrado_ingresar` varchar(255) NOT NULL,
  `c_nivel` varchar(255) NOT NULL,
  `c_respuestas` varchar(512) NOT NULL,
  `b_completo` tinyint(1) NOT NULL,
  `d_creacion` timestamp NOT NULL,
  `d_modificacion` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `id_usuario` (`id_usuario`),
  KEY `idx_usuario_datos_alumno` (`id_usuario`),
  CONSTRAINT `fk_guarda_datos_respuestas` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
 
   
  INSERT INTO `usuario_procesa_datos` (`id_usuario`, `c_apPaterno`, `c_apMaterno`, `c_nombres`, `c_sexo`, `c_num_cuenta`,
`c_posgrado_ingresar`, `c_nivel`, `c_respuestas`, `b_completo`, `d_creacion`, `d_modificacion`)
VALUES
(id,paterno,materno,nombres,sexo,
num_cuenta,posgrado,nivel,@out_value, 1, now(),now());
     
end if;
     

       
  END LOOP;

  CLOSE cur;
 
END$$
DELIMITER ;
