import datetime
import os
import urllib.parse
from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def create_app():
      app = Flask(__name__)
      mongoTable = os.getenv("TABLE")
      mongoUser = os.getenv("USER")
      mongoPassword = os.getenv("PASSWORD")

      escaped_user = urllib.parse.quote_plus(mongoUser)
      escaped_password = urllib.parse.quote_plus(mongoPassword)

      #f"mongodb+srv://{usaurio}:{senha}@aplicacaomicroblog.5ptsi6w.mongodb.net/"
      cliente = MongoClient(f'mongodb+srv://{escaped_user}:{escaped_password}@{mongoTable}.5ptsi6w.mongodb.net/')
      app.db = cliente.microblog
      entradas = []

      @app.route("/", methods=['GET', 'POST'])
      def home():
            if request.method == 'POST':
                  entrada_conteudo = request.form.get('conteudo')
                  data_fomatada = datetime.datetime.today().strftime('%Y-%m-%d')
                  entradas.append((entrada_conteudo, data_fomatada))
                  app.db.entradas.insert_one({'conteudo': entrada_conteudo, 'data': data_fomatada})
            
            entrada_com_data = [
                  (
                        entrada['conteudo'],
                        entrada['data'], 
                        datetime.datetime.strptime(entrada['data'], "%Y-%m-%d").strftime("%b %d")
                  )
                  for entrada in app.db.entradas.find({})
            ]
            return render_template('home.html', entradas=entrada_com_data)
      
      return app

if __name__ == "__main__":
      app = create_app()
      app.run()
