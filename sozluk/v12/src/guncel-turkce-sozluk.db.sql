BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "ornek" (
	"ornek_id"	INTEGER NOT NULL,
	"anlam_id"	INTEGER NOT NULL,
	"ornek_sira"	INTEGER NOT NULL,
	"ornek"	TEXT,
	"kac"	INTEGER NOT NULL,
	"yazar_id"	INTEGER,
	"yazar_vd"	TEXT,
	PRIMARY KEY("ornek_id"),
	FOREIGN KEY("anlam_id") REFERENCES "anlam"("anlam_id"),
	FOREIGN KEY("yazar_id") REFERENCES "yazar"("yazar_id")
);
CREATE TABLE IF NOT EXISTS "anlam" (
	"anlam_id"	INTEGER NOT NULL,
	"madde_id"	INTEGER NOT NULL,
	"anlam_sira"	INTEGER NOT NULL,
	"fiil"	INTEGER NOT NULL,
	"tipkes"	INTEGER NOT NULL,
	"anlam"	TEXT NOT NULL,
	"gos"	INTEGER NOT NULL,
	PRIMARY KEY("anlam_id"),
	FOREIGN KEY("madde_id") REFERENCES "madde"("madde_id")
);
CREATE TABLE IF NOT EXISTS "anlam_ozellik" (
	"anlam_id"	INTEGER NOT NULL,
	"ozellik_id"	INTEGER NOT NULL,
	FOREIGN KEY("ozellik_id") REFERENCES "ozellik"("ozellik_id"),
	FOREIGN KEY("anlam_id") REFERENCES "anlam"("anlam_id")
);
CREATE TABLE IF NOT EXISTS "atasozu" (
	"madde_id"	INTEGER NOT NULL,
	"madde"	TEXT NOT NULL,
	"on_taki" TEXT,
	PRIMARY KEY("madde_id"),
	FOREIGN KEY("madde_id") REFERENCES "madde"("madde_id")
);
CREATE TABLE IF NOT EXISTS "madde" (
	"madde_id"	INTEGER NOT NULL,
	"kac"	INTEGER NOT NULL,
	"kelime_no"	INTEGER NOT NULL,
	"cesit"	INTEGER NOT NULL,
	"anlam_gor"	INTEGER NOT NULL,
	"on_taki"	TEXT,
	"madde"	TEXT NOT NULL,
	"cesit_say"	INTEGER NOT NULL,
	"anlam_say"	INTEGER NOT NULL,
	"taki"	TEXT,
	"cogul_mu"	INTEGER NOT NULL,
	"ozel_mi"	INTEGER NOT NULL,
	"lisan_kodu"	INTEGER NOT NULL,
	"lisan"	TEXT,
	"telaffuz"	TEXT,
	"birlesikler"	TEXT,
	"font"	TEXT,
	"madde_duz"	TEXT NOT NULL,
	"gosterim_tarihi"	TEXT,
	"egik_mi"	INTEGER NOT NULL,
	PRIMARY KEY("madde_id")
);
CREATE TABLE IF NOT EXISTS "ozellik" (
	"ozellik_id"	INTEGER NOT NULL,
	"tur"	INTEGER NOT NULL,
	"tam_adi"	TEXT NOT NULL,
	"kisa_adi"	TEXT NOT NULL,
	"ekno"	INTEGER NOT NULL,
	PRIMARY KEY("ozellik_id")
);
CREATE TABLE IF NOT EXISTS "yazar" (
	"yazar_id"	INTEGER NOT NULL,
	"tam_adi"	TEXT NOT NULL,
	"kisa_adi"	TEXT NOT NULL,
	"ekno"	INTEGER NOT NULL,
	PRIMARY KEY("yazar_id")
);
CREATE TABLE IF NOT EXISTS "madde_atasozu" (
	"madde_id"	INTEGER NOT NULL,
	"atasozu_madde_id"	INTEGER NOT NULL,
	FOREIGN KEY("madde_id") REFERENCES "madde"("madde_id"),
	FOREIGN KEY("atasozu_madde_id") REFERENCES "atasozu"("madde_id")
);
COMMIT;
