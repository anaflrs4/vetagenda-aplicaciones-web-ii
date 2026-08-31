-- SQL generado por Django para el esquema de VetAgenda
-- Migracion 0001: modelos principales
BEGIN;
--
-- Create model Propietario
--
CREATE TABLE "citas_propietario" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "nombre_completo" varchar(120) NOT NULL, "telefono" varchar(25) NOT NULL, "email" varchar(254) NOT NULL, "fecha_registro" datetime NOT NULL);
--
-- Create model Veterinario
--
CREATE TABLE "citas_veterinario" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "nombre_completo" varchar(120) NOT NULL, "especialidad" varchar(100) NOT NULL, "telefono" varchar(25) NOT NULL, "email" varchar(254) NOT NULL, "activo" bool NOT NULL);
--
-- Create model Mascota
--
CREATE TABLE "citas_mascota" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "nombre" varchar(80) NOT NULL, "especie" varchar(20) NOT NULL, "raza" varchar(80) NOT NULL, "fecha_nacimiento" date NULL, "peso_kg" decimal NULL, "notas" text NOT NULL, "fecha_registro" datetime NOT NULL, "propietario_id" bigint NOT NULL REFERENCES "citas_propietario" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Cita
--
CREATE TABLE "citas_cita" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "fecha" date NOT NULL, "hora" time NOT NULL, "motivo" varchar(180) NOT NULL, "estado" varchar(20) NOT NULL, "observaciones" text NOT NULL, "creado_en" datetime NOT NULL, "actualizado_en" datetime NOT NULL, "mascota_id" bigint NOT NULL REFERENCES "citas_mascota" ("id") DEFERRABLE INITIALLY DEFERRED, "veterinario_id" bigint NOT NULL REFERENCES "citas_veterinario" ("id") DEFERRABLE INITIALLY DEFERRED, CONSTRAINT "cita_unica_por_veterinario_horario" UNIQUE ("veterinario_id", "fecha", "hora"));
CREATE INDEX "citas_mascota_propietario_id_dae35364" ON "citas_mascota" ("propietario_id");
CREATE INDEX "citas_cita_mascota_id_57d42afa" ON "citas_cita" ("mascota_id");
CREATE INDEX "citas_cita_veterinario_id_7789b1f4" ON "citas_cita" ("veterinario_id");
COMMIT;
-- Migracion 0002: duracion de las citas
BEGIN;
--
-- Add field duracion_minutos to cita
--
CREATE TABLE "new__citas_cita" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "duracion_minutos" smallint unsigned NOT NULL CHECK ("duracion_minutos" >= 0), "fecha" date NOT NULL, "hora" time NOT NULL, "motivo" varchar(180) NOT NULL, "estado" varchar(20) NOT NULL, "observaciones" text NOT NULL, "creado_en" datetime NOT NULL, "actualizado_en" datetime NOT NULL, "mascota_id" bigint NOT NULL REFERENCES "citas_mascota" ("id") DEFERRABLE INITIALLY DEFERRED, "veterinario_id" bigint NOT NULL REFERENCES "citas_veterinario" ("id") DEFERRABLE INITIALLY DEFERRED, CONSTRAINT "cita_unica_por_veterinario_horario" UNIQUE ("veterinario_id", "fecha", "hora"));
INSERT INTO "new__citas_cita" ("id", "fecha", "hora", "motivo", "estado", "observaciones", "creado_en", "actualizado_en", "mascota_id", "veterinario_id", "duracion_minutos") SELECT "id", "fecha", "hora", "motivo", "estado", "observaciones", "creado_en", "actualizado_en", "mascota_id", "veterinario_id", 30 FROM "citas_cita";
DROP TABLE "citas_cita";
ALTER TABLE "new__citas_cita" RENAME TO "citas_cita";
CREATE INDEX "citas_cita_mascota_id_57d42afa" ON "citas_cita" ("mascota_id");
CREATE INDEX "citas_cita_veterinario_id_7789b1f4" ON "citas_cita" ("veterinario_id");
COMMIT;
-- Migracion 0003: restriccion de citas activas
BEGIN;
--
-- Remove constraint cita_unica_por_veterinario_horario from model cita
--
CREATE TABLE "new__citas_cita" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "fecha" date NOT NULL, "hora" time NOT NULL, "motivo" varchar(180) NOT NULL, "estado" varchar(20) NOT NULL, "observaciones" text NOT NULL, "creado_en" datetime NOT NULL, "actualizado_en" datetime NOT NULL, "mascota_id" bigint NOT NULL REFERENCES "citas_mascota" ("id") DEFERRABLE INITIALLY DEFERRED, "veterinario_id" bigint NOT NULL REFERENCES "citas_veterinario" ("id") DEFERRABLE INITIALLY DEFERRED, "duracion_minutos" smallint unsigned NOT NULL CHECK ("duracion_minutos" >= 0));
INSERT INTO "new__citas_cita" ("id", "fecha", "hora", "motivo", "estado", "observaciones", "creado_en", "actualizado_en", "mascota_id", "veterinario_id", "duracion_minutos") SELECT "id", "fecha", "hora", "motivo", "estado", "observaciones", "creado_en", "actualizado_en", "mascota_id", "veterinario_id", "duracion_minutos" FROM "citas_cita";
DROP TABLE "citas_cita";
ALTER TABLE "new__citas_cita" RENAME TO "citas_cita";
CREATE INDEX "citas_cita_mascota_id_57d42afa" ON "citas_cita" ("mascota_id");
CREATE INDEX "citas_cita_veterinario_id_7789b1f4" ON "citas_cita" ("veterinario_id");
--
-- Create constraint cita_activa_unica_por_veterinario_horario on model cita
--
CREATE UNIQUE INDEX "cita_activa_unica_por_veterinario_horario" ON "citas_cita" ("veterinario_id", "fecha", "hora") WHERE NOT ("estado" = 'cancelada');
COMMIT;
