from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime


# ==========================================
# INISIALISASI FLASK
# ==========================================

app = Flask(__name__)


# ==========================================
# PATH FOLDER
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


# ==========================================
# DATABASE JSON TUNGGAL
# ==========================================

DATABASE_FILE = os.path.join(
    BASE_DIR,
    "database.json"
)


# ==========================================
# BUAT DATABASE JIKA BELUM ADA
# ==========================================

if not os.path.exists(
    DATABASE_FILE
):

    with open(
        DATABASE_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            {
                "transaksi": []
            },
            file,
            ensure_ascii=False,
            indent=4
        )


# ==========================================
# FUNGSI BACA DATABASE
# ==========================================

def baca_database():

    try:

        with open(
            DATABASE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(
                file
            )


        # PASTIKAN FORMAT BENAR

        if "transaksi" not in data:

            data["transaksi"] = []


        return data


    except Exception as error:

        print(
            "ERROR BACA DATABASE:",
            error
        )


        return {

            "transaksi": []

        }


# ==========================================
# FUNGSI SIMPAN DATABASE
# ==========================================

def simpan_database(data):

    try:

        with open(
            DATABASE_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4
            )


        return True


    except Exception as error:

        print(
            "ERROR SIMPAN DATABASE:",
            error
        )


        return False


# ==========================================
# HALAMAN UTAMA
# ==========================================

@app.route("/")
def index():

    return render_template(
        "BKU.html"
    )


# ==========================================
# HALAMAN BKU
# ==========================================

@app.route("/bku")
def halaman_bku():

    return render_template(
        "BKU.html"
    )


# ==========================================
# HALAMAN BKT
# ==========================================

@app.route("/bkt")
def halaman_bkt():

    return render_template(
        "BKT.html"
    )


# ==========================================
# HALAMAN BKP
# ==========================================

@app.route("/bkp")
def halaman_bkp():

    return render_template(
        "BKP.html"
    )


# ==========================================
# HALAMAN KWITANSI
# ==========================================

@app.route("/kwitansi")
def halaman_kwitansi():

    return render_template(
        "kwitansi.html"
    )


# ==========================================
# API STATUS SERVER
# ==========================================

@app.route(
    "/api/status",
    methods=["GET"]
)
def status_server():

    return jsonify(
        {
            "status": "online",

            "database":
            "database.json",

            "waktu":
            datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            )
        }
    )


# ==========================================
# API
# AMBIL SEMUA DATA
#
# DIGUNAKAN:
# BKU
# BKT
# BKP
# ==========================================

@app.route(
    "/api/transaksi",
    methods=["GET"]
)
def ambil_semua_transaksi():

    data = baca_database()


    return jsonify(
        data
    )


# ==========================================
# API
# TAMBAH TRANSAKSI
#
# HANYA BKU
# ==========================================

@app.route(
    "/api/transaksi",
    methods=["POST"]
)
def tambah_transaksi():

    try:

        transaksi_baru = request.get_json()


        if not transaksi_baru:

            return jsonify(
                {
                    "status": "error",
                    "message":
                    "Data transaksi tidak ditemukan"
                }
            ), 400


        # ======================================
        # BACA DATABASE
        # ======================================

        database = baca_database()


        # ======================================
        # BUAT ID UNIK
        # ======================================

        transaksi_baru["id"] = (

            datetime.now()
            .strftime(
                "%Y%m%d%H%M%S%f"
            )

        )


        # ======================================
        # WAKTU DIBUAT
        # ======================================

        transaksi_baru["created_at"] = (

            datetime.now()
            .strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        )


        # ======================================
        # TAMBAHKAN TRANSAKSI
        # ======================================

        database[
            "transaksi"
        ].append(
            transaksi_baru
        )


        # ======================================
        # SIMPAN DATABASE
        # ======================================

        simpan_database(
            database
        )


        return jsonify(
            {
                "status":
                "success",

                "message":
                "Transaksi berhasil ditambahkan",

                "data":
                transaksi_baru
            }
        )


    except Exception as error:

        return jsonify(
            {
                "status":
                "error",

                "message":
                str(error)
            }
        ), 500


# ==========================================
# API
# UPDATE TRANSAKSI
#
# HANYA BKU
# ==========================================

@app.route(
    "/api/transaksi/<id_transaksi>",
    methods=["PUT"]
)
def update_transaksi(
    id_transaksi
):

    try:

        data_update = request.get_json()


        if not data_update:

            return jsonify(
                {
                    "status":
                    "error",

                    "message":
                    "Data update tidak ditemukan"
                }
            ), 400


        # ======================================
        # BACA DATABASE
        # ======================================

        database = baca_database()


        ditemukan = False


        # ======================================
        # CARI TRANSAKSI
        # ======================================

        for index, transaksi in enumerate(
            database["transaksi"]
        ):


            if str(
                transaksi.get("id")
            ) == str(
                id_transaksi
            ):


                # ID TETAP

                data_update["id"] = (
                    id_transaksi
                )


                # CREATED AT TETAP

                data_update[
                    "created_at"
                ] = transaksi.get(
                    "created_at",
                    ""
                )


                # WAKTU UPDATE

                data_update[
                    "updated_at"
                ] = (

                    datetime.now()
                    .strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )

                )


                database[
                    "transaksi"
                ][index] = (
                    data_update
                )


                ditemukan = True


                break


        # ======================================
        # JIKA TIDAK DITEMUKAN
        # ======================================

        if not ditemukan:

            return jsonify(
                {
                    "status":
                    "error",

                    "message":
                    "Transaksi tidak ditemukan"
                }
            ), 404


        # ======================================
        # SIMPAN DATABASE
        # ======================================

        simpan_database(
            database
        )


        return jsonify(
            {
                "status":
                "success",

                "message":
                "Transaksi berhasil diperbarui"
            }
        )


    except Exception as error:

        return jsonify(
            {
                "status":
                "error",

                "message":
                str(error)
            }
        ), 500


# ==========================================
# API
# HAPUS TRANSAKSI
#
# HANYA BKU
# ==========================================

@app.route(
    "/api/transaksi/<id_transaksi>",
    methods=["DELETE"]
)
def hapus_transaksi(
    id_transaksi
):

    try:

        # ======================================
        # BACA DATABASE
        # ======================================

        database = baca_database()


        transaksi_baru = []


        ditemukan = False


        # ======================================
        # FILTER DATA
        # ======================================

        for transaksi in database[
            "transaksi"
        ]:


            if str(
                transaksi.get("id")
            ) == str(
                id_transaksi
            ):


                ditemukan = True

                continue


            transaksi_baru.append(
                transaksi
            )


        # ======================================
        # JIKA DATA TIDAK ADA
        # ======================================

        if not ditemukan:

            return jsonify(
                {
                    "status":
                    "error",

                    "message":
                    "Transaksi tidak ditemukan"
                }
            ), 404


        # ======================================
        # UPDATE DATABASE
        # ======================================

        database[
            "transaksi"
        ] = transaksi_baru


        # ======================================
        # SIMPAN
        # ======================================

        simpan_database(
            database
        )


        return jsonify(
            {
                "status":
                "success",

                "message":
                "Transaksi berhasil dihapus"
            }
        )


    except Exception as error:

        return jsonify(
            {
                "status":
                "error",

                "message":
                str(error)
            }
        ), 500


# ==========================================
# API
# DATA BKT
#
# HANYA READ
# DATABASE.JSON
# ==========================================

@app.route(
    "/api/bkt",
    methods=["GET"]
)
def ambil_data_bkt():

    database = baca_database()


    transaksi_bkt = []


    nomor = 1


    # ======================================
    # AMBIL DATA DARI DATABASE
    # ======================================

    for data in database.get(
        "transaksi",
        []
    ):


        penarikan = float(
            data.get(
                "penarikan",
                0
            ) or 0
        )


        pengeluaran = float(
            data.get(
                "pengeluaran",
                0
            ) or 0
        )


        ppn = float(
            data.get(
                "ppn",
                0
            ) or 0
        )


        pph22 = float(
            data.get(
                "pph22",
                0
            ) or 0
        )


        # ==================================
        # FILTER
        #
        # BKT TIDAK AMBIL PENERIMAAN BKU
        #
        # YANG DIAMBIL:
        #
        # PENARIKAN
        # PENGELUARAN
        # PPN
        # PPH22
        # ==================================

        if (

            penarikan > 0

            or

            pengeluaran > 0

            or

            ppn > 0

            or

            pph22 > 0

        ):


            # ==============================
            # PENARIKAN BKU
            # MENJADI
            # PENERIMAAN BKT
            # ==============================

            penerimaan_bkt = (
                penarikan
            )


            # ==============================
            # PENGELUARAN BKT
            # ==============================

            pengeluaran_bkt = (

                pengeluaran

                +

                ppn

                +

                pph22

            )


            # ==============================
            # NETTO BKT
            # ==============================

            netto = (

                penerimaan_bkt

                -

                pengeluaran_bkt

            )


            # ==============================
            # SIMPAN KE ARRAY SEMENTARA
            # TIDAK KE DATABASE
            # ==============================

            transaksi_bkt.append(

                {

                    "id":
                    data.get(
                        "id"
                    ),

                    "nomor":
                    nomor,

                    "tanggal":
                    data.get(
                        "tanggal",
                        ""
                    ),

                    "uraian":
                    data.get(
                        "uraian",
                        ""
                    ),

                    "nomorBukti":
                    data.get(
                        "nomorBukti",
                        ""
                    ),

                    "penerimaan":
                    penerimaan_bkt,

                    "pengeluaran":
                    pengeluaran_bkt,

                    "netto":
                    netto

                }

            )


            nomor += 1


    # ======================================
    # RETURN DATA SAJA
    # TIDAK SIMPAN KE JSON
    # ======================================

    return jsonify(

        {

            "transaksi":
            transaksi_bkt

        }

    )


# ==========================================
# API
# DATA BKP
#
# HANYA READ
# DATABASE.JSON
# ==========================================

@app.route(
    "/api/bkp",
    methods=["GET"]
)
def ambil_data_bkp():

    database = baca_database()


    transaksi_bkp = []


    nomor = 1


    # ======================================
    # AMBIL DATA DATABASE
    # ======================================

    for data in database.get(
        "transaksi",
        []
    ):


        ppn = float(

            data.get(
                "ppn",
                0
            ) or 0

        )


        pph22 = float(

            data.get(
                "pph22",
                0
            ) or 0

        )


        # ==================================
        # HANYA DATA PAJAK
        # ==================================

        if (

            ppn > 0

            or

            pph22 > 0

        ):


            total = (

                ppn

                +

                pph22

            )


            transaksi_bkp.append(

                {

                    "id":
                    data.get(
                        "id"
                    ),

                    "nomor":
                    nomor,

                    "tanggal":
                    data.get(
                        "tanggal",
                        ""
                    ),

                    "uraian":
                    data.get(
                        "uraian",
                        ""
                    ),

                    "ppn":
                    ppn,

                    "pph22":
                    pph22,

                    "total":
                    total

                }

            )


            nomor += 1


    # ======================================
    # RETURN DATA
    # TANPA EDIT DATABASE
    # ======================================

    return jsonify(

        {

            "transaksi":
            transaksi_bkp

        }

    )


# ==========================================
# API
# AMBIL SATU TRANSAKSI
#
# UNTUK KWITANSI
# ==========================================

@app.route(
    "/api/transaksi/<id_transaksi>",
    methods=["GET"]
)
def ambil_satu_transaksi(
    id_transaksi
):

    database = baca_database()


    for transaksi in database[
        "transaksi"
    ]:


        if str(
            transaksi.get("id")
        ) == str(
            id_transaksi
        ):


            return jsonify(

                {

                    "status":
                    "success",

                    "data":
                    transaksi

                }

            )


    return jsonify(

        {

            "status":
            "error",

            "message":
            "Transaksi tidak ditemukan"

        }

    ), 404


# ==========================================
# JALANKAN SERVER
# ==========================================

if __name__ == "__main__":

    print(
        ""
    )

    print(
        "======================================"
    )

    print(
        "SISTEM KEUANGAN BUMDES"
    )

    print(
        "SERVER BERJALAN"
    )

    print(
        "======================================"
    )

    print(
        "BKU:"
    )

    print(
        "http://127.0.0.1:5000/bku"
    )

    print(
        ""
    )

    print(
        "BKT:"
    )

    print(
        "http://127.0.0.1:5000/bkt"
    )

    print(
        ""
    )

    print(
        "BKP:"
    )

    print(
        "http://127.0.0.1:5000/bkp"
    )

    print(
        ""
    )

    print(
        "KWITANSI:"
    )

    print(
        "http://127.0.0.1:5000/kwitansi"
    )

    print(
        "======================================"
    )


    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True,

        threaded=True

    )
