""" MongoDB icerisindeki kayitlari SQLite veritabanina aktarir """
from pymongo import MongoClient
import sqlite3

CLIENT = MongoClient("localhost", 27017)
MONGO_TOPICS = CLIENT.gts.maddeler

def create_connection(db_file):
  """ sqlite connectionu olusturur """
  try:
      conn = sqlite3.connect(db_file)
      return conn
  except Exception as e:
      print(e)

  return None

def insert_anlam(conn, anlam):
  """ anlami veritabanina ekler """
  sql = """INSERT INTO anlam(anlam_id,madde_id,anlam_sira,fiil,tipkes,anlam,gos)
           VALUES (?,?,?,?,?,?,?)"""
  arr = (anlam["anlam_id"],anlam["madde_id"],anlam["anlam_sira"],anlam["fiil"],anlam["tipkes"],anlam["anlam"],anlam["gos"])
  cur = conn.cursor()
  cur.execute(sql, arr)

  if "ozelliklerListe" in anlam:
    insert_ozellikler(conn, anlam["anlam_id"], anlam["ozelliklerListe"])

  if "orneklerListe" in anlam:
    insert_ornekler(conn, anlam["orneklerListe"])

  return cur.lastrowid

def insert_anlamlar(conn, madde):
  """ anlamlari veritabanina ekler """
  if "anlamlarListe" not in madde:
    return None

  anlamlar = madde["anlamlarListe"]
  for anlam in anlamlar:
    insert_anlam(conn, anlam)

def insert_anlam_ozellik(conn, anlam_id, ozellik_id):
  """ anlam_ozellik ilisiklisini veritanina ekler """
  sql = """INSERT INTO anlam_ozellik(anlam_id, ozellik_id) 
           VALUES (?,?)"""
  arr = (anlam_id, ozellik_id)
  cur = conn.cursor()
  cur.execute(sql, arr)

def insert_atasozu(conn, atasozu):
  """ atasozunu veritabanina ekler """
  sql = """INSERT OR REPLACE INTO atasozu(madde_id,madde) 
           VALUES (?,?)"""
  arr = (atasozu["madde_id"],atasozu["madde"])
  cur = conn.cursor()
  cur.execute(sql, arr)

def insert_atasozleri(conn, madde):
  """ atasozlerini veritabanina ekler """
  if "atasozu" not in madde:
    return None

  atasozleri = madde["atasozu"]
  for atasozu in atasozleri:
    insert_atasozu(conn, atasozu)
    insert_madde_atasozu(conn, madde["madde_id"], atasozu["madde_id"])

def insert_madde(conn, madde):
  """ maddeyi veritabanina ekler """
  sql = """INSERT INTO madde(madde_id,kac,kelime_no,cesit,anlam_gor,on_taki,madde,cesit_say,anlam_say,taki,cogul_mu,ozel_mi,lisan_kodu,lisan,telaffuz,birlesikler,font,madde_duz,gosterim_tarihi)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
  arr = (madde.get("madde_id"),madde.get("kac"),madde.get("kelime_no"),madde.get("cesit"),madde.get("anlam_gor"),madde.get("on_taki"),madde.get("madde"),madde.get("cesit_say"),madde.get("anlam_say"),madde.get("taki"),madde.get("cogul_mu"),madde.get("ozel_mi"),madde.get("lisan_kodu"),madde.get("lisan"),madde.get("telaffuz"),madde.get("birlesikler"),madde.get("font"),madde.get("madde_duz"),madde.get("gosterim_tarihi"))
  cur = conn.cursor()
  cur.execute(sql, arr)
  return cur.lastrowid

def insert_madde_atasozu(conn, madde_id, atasozu_madde_id):
  """ madde_atasozu iliskisini kurar """
  sql = """INSERT INTO madde_atasozu(madde_id, atasozu_madde_id) 
           VALUES (?,?)"""
  arr = (madde_id, atasozu_madde_id)
  cur = conn.cursor()
  cur.execute(sql, arr)

def insert_ornek(conn, ornek):
  """ ornegi veritabanina ekler """
  if "yazar" in ornek:
    insert_yazarlar(conn, ornek["yazar"])

  sql = """INSERT INTO ornek(ornek_id,anlam_id,ornek_sira,ornek,kac,yazar_id)
           VALUES (?,?,?,?,?,?)"""

  yazar_id = None
  if ornek["yazar_id"] and ornek["yazar_id"] != "0":
    yazar_id = ornek["yazar_id"]

  arr = (ornek["ornek_id"],ornek["anlam_id"],ornek["ornek_sira"],ornek["ornek"],ornek["kac"],yazar_id)
  cur = conn.cursor()
  cur.execute(sql, arr)

def insert_ornekler(conn, ornekler):
  """ ornekleri veritabanina ekler """
  if not ornekler:
    return None

  for ornek in ornekler:
    insert_ornek(conn, ornek)

def insert_ozellik(conn, ozellik):
  """ ozelligi veritabanina ekler """
  sql = """INSERT OR REPLACE INTO ozellik(ozellik_id,tur,tam_adi,kisa_adi,ekno) 
           VALUES (?,?,?,?,?)"""
  arr = (ozellik["ozellik_id"],ozellik["tur"],ozellik["tam_adi"],ozellik["kisa_adi"],ozellik["ekno"])
  cur = conn.cursor()
  cur.execute(sql, arr)

def insert_ozellikler(conn, anlam_id, ozellikler):
  """ ozellikleri veritabanina ekler """
  if not ozellikler:
    return None

  for ozellik in ozellikler:
    insert_ozellik(conn, ozellik)
    insert_anlam_ozellik(conn, anlam_id, ozellik["ozellik_id"])

def insert_yazar(conn, yazar):
  """ yazari veritabanina ekler """
  sql = """INSERT OR REPLACE INTO yazar(yazar_id,tam_adi,kisa_adi,ekno) 
           VALUES (?,?,?,?)"""
  arr = (yazar["yazar_id"],yazar["tam_adi"],yazar["kisa_adi"],yazar["ekno"])
  cur = conn.cursor()
  cur.execute(sql, arr)

def insert_yazarlar(conn, yazarlar):
  """ yazarlari veritabanina ekler """
  if not yazarlar:
    return None

  for yazar in yazarlar:
    insert_yazar(conn, yazar)

def execute():
  """ ana method """
  for madde in MONGO_TOPICS.find():
    conn = create_connection("guncel-turkce-sozluk.db")

    insert_madde(conn, madde)
    insert_anlamlar(conn, madde)
    insert_atasozleri(conn, madde)

    conn.commit()

if __name__ == "__main__":
    execute()
