
CREATE TABLE USUARIO (
   id                NUMBER PRIMARY KEY,
   nombre_usuario    VARCHAR2(50) NOT NULL UNIQUE,
   clave             VARCHAR2(255) NOT NULL, -- hash de contraseña
   nombre            VARCHAR2(50) NOT NULL,
   apellido          VARCHAR2(50) NOT NULL,
   fecha_nacimiento  DATE,
   telefono          VARCHAR2(20),
   email             VARCHAR2(100),
   tipo              VARCHAR2(20) DEFAULT 'PACIENTE'
);
--secuencia para la tabla USUARIO
CREATE SEQUENCE usuario_seq
START WITH 1
INCREMENT BY 1
NOCACHE
NOCYCLE;

-- trigger auto-id para la tabla USUARIO
CREATE OR REPLACE TRIGGER trg_usuario_id
BEFORE INSERT ON USUARIO
FOR EACH ROW
BEGIN
   IF :NEW.id IS NULL THEN
      SELECT usuario_seq.NEXTVAL
      INTO :NEW.id
      FROM dual;
   END IF;
END;
/
--paciente
CREATE TABLE PACIENTE (
   id NUMBER PRIMARY KEY,
   comuna VARCHAR2(100),
   fecha_primera_visita DATE
);

ALTER TABLE PACIENTE
   ADD CONSTRAINT fk_paciente_usuario
   FOREIGN KEY (id) REFERENCES USUARIO(id)
   ON DELETE CASCADE;


--medico
CREATE TABLE MEDICO (
   id NUMBER PRIMARY KEY,
   especialidad VARCHAR2(100),
   horario_atencion VARCHAR2(50),
   fecha_ingreso DATE,
   CONSTRAINT fk_medico_usuario
      FOREIGN KEY (id)
      REFERENCES USUARIO(id)
      ON DELETE CASCADE
);


-- recetas
CREATE TABLE RECETA (
   id NUMBER PRIMARY KEY,
   id_paciente NUMBER NOT NULL,
   id_medico NUMBER NOT NULL,
   descripcion VARCHAR2(500),
   medicamentos_recetados VARCHAR2(1000),
   costo_clp NUMBER(10,2),
   fecha DATE,
   CONSTRAINT fk_receta_paciente
      FOREIGN KEY (id_paciente)
      REFERENCES PACIENTE(id)
      ON DELETE CASCADE,
   CONSTRAINT fk_receta_medico
      FOREIGN KEY (id_medico)
      REFERENCES MEDICO(id)
      ON DELETE CASCADE
);


-- Consultas
CREATE TABLE CONSULTA (
   id NUMBER PRIMARY KEY,
   id_paciente NUMBER NOT NULL,
   id_medico NUMBER NOT NULL,
   id_receta NUMBER,
   fecha DATE,
   comentarios VARCHAR2(1000),
   valor NUMBER(10,2),
   CONSTRAINT fk_consulta_paciente
      FOREIGN KEY (id_paciente)
      REFERENCES PACIENTE(id)
      ON DELETE CASCADE,
   CONSTRAINT fk_consulta_medico
      FOREIGN KEY (id_medico)
      REFERENCES MEDICO(id)
      ON DELETE CASCADE,
   CONSTRAINT fk_consulta_receta
      FOREIGN KEY (id_receta)
      REFERENCES RECETA(id)
      ON DELETE SET NULL
);



-- Insumos
CREATE TABLE INSUMO (
   id NUMBER PRIMARY KEY,
   nombre VARCHAR2(100) NOT NULL,
   tipo VARCHAR2(50),
   stock NUMBER,
   costo_usd NUMBER(10,2)
);


-- ==============================
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE AGENDA CASCADE CONSTRAINTS';
EXCEPTION
   WHEN OTHERS THEN
      IF SQLCODE != -942 THEN -- ORA-00942: tabla no existe
         RAISE;
      END IF;
END;
/

-- Agenda
CREATE TABLE AGENDA (
   id NUMBER PRIMARY KEY,
   id_paciente NUMBER NOT NULL,
   id_medico NUMBER NOT NULL,
   fecha_consulta DATE,
   estado VARCHAR2(50),
   CONSTRAINT fk_agenda_paciente
      FOREIGN KEY (id_paciente)
      REFERENCES PACIENTE(id)
      ON DELETE CASCADE,
   CONSTRAINT fk_agenda_medico
      FOREIGN KEY (id_medico)
      REFERENCES MEDICO(id)
      ON DELETE CASCADE
);
