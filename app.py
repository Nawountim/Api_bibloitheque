import os

from ast import Or

from flask import Flask , render_template,request,redirect,url_for,abort,jsonify

from flask_sqlalchemy import SQLAlchemy

from urllib.parse import quote_plus

from dotenv import load_dotenv

from flask_cors import CORS

load_dotenv()

app = Flask(__name__)


user = quote_plus(os.getenv('db_user'))
motdepasse = quote_plus(os.getenv('db_password'))
host = quote_plus( os.getenv('hostname'))
port = quote_plus( os.getenv('port'))
bdd = quote_plus( os.getenv('db_name'))


#########################################################################
#
#               Endpoint Definition de la chaine de connexion
#
#########################################################################
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{}:{}@{}:{}/{}'.format(user,motdepasse,host,port,bdd)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)

#########################################################################
#
#               Endpoint Creation des classes Livre et Categorie
#
#########################################################################
 

class Livre(db.Model):
            __tablename__='livres'
            Id = db.Column(db.Integer,primary_key= True)
            isbn = db.Column(db.String(50),nullable=False)
            titre = db.Column(db.String(50),nullable=False)
            dat_publication = db.Column(db.DateTime,nullable=False) 
            auteur = db.Column(db.String(50),nullable=False)   
            editeur = db.Column(db.String(50),nullable=False)   
            categorie_id = db.Column(db.Integer,db.ForeignKey('categories.id'),nullable= False)
            
            def format(self):
                return{
                    
                    'Id':self.Id,
                    'Code ISBN':self.isbn,
                    'Titre':self.titre,
                    'Date de publication':self.dat_publication,
                    'Auteur':self.auteur,
                    'Editeur':self.editeur,
                    'Identifiant de sa categorie':self.categorie_id,

                }
            def delete(self):
                db.session.delete(self)
                db.session.commit()      
            def update(self):
                db.session.commit()
                
class Categorie(db.Model):
            __tablename__='categories'
            id = db.Column(db.Integer,primary_key= True)
            libelle_categorie = db.Column(db.String(50),nullable=False)
            livres = db.relationship('Livre',backref='categories',lazy=True)
            
            def format(self):
                return{
                    
                    'Id':self.id,
                    'Libelle':self.libelle_categorie,
                    }
            def delete(self):
                db.session.delete(self)
                db.session.commit()  
                
            def update(self):
                db.session.commit() 
                
         
db.create_all()

#########################################################################
#
#               Endpoint Liste de tous les livres
#
#########################################################################
 
@app.route('/livres')
def Liste_livre():
    livres=Livre.query.all()
    formated_livres = [ et.format() for et in livres]
    if livres is None:
        abort(404)
    else:
        return jsonify({
        'Success': True,
        'total': len(livres),
        "Ensemble des livres":  formated_livres
         })
        
#########################################################################
#
#               Endpoint recuperer un livre en particulier
#
#########################################################################
         

@app.route('/livres/<int:id>')
def Un_livre(id):
    livre=Livre.query.get(id)
    if livre is None:
        abort(404)
    else:
        return jsonify({
        'Success': True,
        'Id selectionné':id,
        "Livre recherché": livre.format()
         })
        
#########################################################################
#
#               Endpoint Liste de toutes les categories
#
#########################################################################
 
@app.route('/categories')
def Liste_Categorie():
    categories=Categorie.query.all()
    formated_categories = [ et.format() for et in categories]
    if categories is None:
        abort(404)
    else:
        return jsonify({
        'Success': True,
        'total': len(categories),
        "Ensemble des catégories":  formated_categories
         })
  
#########################################################################
#
#               Endpoint recuperer une catégorie en particulier
#
#########################################################################
          
  
@app.route('/categories/<int:id>')
def Une_categorie(id):
    c=Categorie.query.get(id)
    if c is None:
        abort(404)
    else:
        return jsonify({
        'Success': True,
        'Id selectionné':id,
        "Categorie recherché": c.format()
         })  
#########################################################################
#
#               Endpoint Ajout d'un Livre depuis un formulaire
#
#########################################################################
 
 
@app.route('/create')
def creer_livre():
    return render_template('Ajout_livre.html') 
   
#########################################################################
#
#               Endpoint Ajout d'une categorie depuis un formulaire
#
#########################################################################
     
    
@app.route('/create_categorie')
def creer_categorie():
    return render_template('Ajout_categorie.html')


#########################################################################
#
#               Endpoint Methode permattant d'ajout du livre
#
#########################################################################
 
    
@app.route('/add', methods=['POST'])
def ajouter_un_livre(): 
    try:
        new_isbn = request.form.get('isbn')   
        new_tit = request.form.get('tit')   
        new_dt = request.form.get('dat_pub')  
        new_auteur = request.form.get('auteur')
        new_editeur = request.form.get('edit')
        new_cate = request.form.get('cate')        
        livre =Livre( isbn=new_isbn, titre=new_tit, dat_publication=new_dt ,auteur=new_auteur ,editeur=new_editeur, categorie_id= new_cate )  
        db.session.add(livre )
        db.session.commit()
        return redirect(url_for('Liste_livre'))   
    except:
        db.session.rollback()   
    finally:
        db.session.close()  
        
#########################################################################
#
#               Endpoint Methode permattant l'ajout de la catégorie

#########################################################################

             
@app.route('/add_categorie', methods=['POST'])
def ajouter_une_categorie(): 
    try:
        new_lib = request.form.get('cat')
        categorie=Categorie( libelle_categorie = new_lib )  
        db.session.add(categorie)
        db.session.commit()
        return redirect(url_for('Liste_Categorie'))            
    except:
        db.session.rollback()   
    finally:
        db.session.close()   
          
#########################################################################
#
#               Endpoint Methode permattant d'avoir l'ensemble des livres d'une catégorie
#
#########################################################################
      
@app.route('/livres/categorie/<int:id>')
def Liste_livres_categorie(id):
    livres = Livre.query.filter(Livre.categorie_id == id)
    categorie = Categorie.query.get(id)
    formated_livres = [ et.format() for et in livres]
    if livres is None or categorie is None:
        abort(404)
    else:
        return jsonify({
        'Success': True,
        "Ensemble des livres":  formated_livres,
        "Categorie selectionée" :categorie.format()
         })        
        
#########################################################################
#
#               Endpoint Suppression de livre
#
#########################################################################
        
@app.route('/livres/<int:id>', methods=['DELETE'])
def supprimer_livre(id): 
    livre=Livre.query.get(id) 
    if livre is None:
        abort(404)   
    else:
        #supprimer la personne
        livre.delete()
        return jsonify({
        'Success': True,
        "Informations sur le livre supprimé": livre.format(),
        'Nombre de livres' : livre.query.count()
    })           
        
#########################################################################
#
#               Endpoint Suppression d'une categorie
#
#########################################################################
        
        
@app.route('/categories/<int:id>', methods=['DELETE'])
def supprimer_categorie(id): 
    c=Categorie.query.get(id) 
    if c is None:
        abort(404)   
    else:
        #supprimer la personne
        c.delete()
        return jsonify({
        'Success': True,
        "Informations sur la Categorie supprimée": c.format(),
        'Nombre de Categories' :c.query.count()
    })  
        
#########################################################################
#
#               Endpoint Methode permattant la modification d'un livre
#
#########################################################################
         
@app.route('/livres/<int:id>', methods=['PUT'])
def modifier_livre(id): 
    l=Livre.query.get(id)
    if l is None:
        abort(404)   
    else:  
        body=request.get_json()
        l.isbn= body.get('ISBN') 
        l.titre = body.get('Titre')    
        l.dat_publication =body.get('Date')
        l.auteur = body.get('Auteur') 
        l.editeur = body.get('Editeur') 
        l.categorie_id = body.get('Code_categorie') 

        l.update() 
    return jsonify({
    'Success': True,
    'Id selectionné':id,
    "Livre modifiéé": l.format(),
    })  
#########################################################################
#
#               Endpoint Methode permattant la modification d'une catégorie
#
#########################################################################
     
@app.route('/categories/<int:id>', methods=['PATCH'])
def modifier_categorie(id): 
    cc=Categorie.query.get(id)
    if cc is None:
        abort(404)   
    else:  
        body=request.get_json()
        cc.libelle_categorie= body.get('Nouveau libellé')                              
        cc.update() 
    return jsonify({
    'Success': True,
    'Id selectionné':id,
    "Categorie modifiéé": cc.format(),
    })  
    
#########################################################################
#
#               Endpoint Methode permattant la modification du titre du livre
#
#########################################################################
         
@app.route('/livres/<int:id>', methods=['PATCH'])
def modifier_titre(id): 
    lv=Livre.query.get(id)
    if lv is None:
        abort(404)   
    else:  
        body = request.get_json()
        lv.titre = body.get('Nouveau titre')                              
        lv.update() 
    return jsonify({
    'Success': True,
    'Id selectionné':id,
    "Livre modifiéé": lv.format(),
    })     

#########################################################################
#
#               Endpoint Methode permattant la modification du code isbn du livre
#
#########################################################################
      
@app.route('/livres/code/<int:id>', methods=['PATCH'])
def modifier_isbn(id): 
    lc=Livre.query.get(id)
    if lc is None:
        abort(404)   
    else:  
        body = request.get_json()
        lc.isbn = body.get('Nouveau code')                              
        lc.update() 
    return jsonify({
    'Success': True,
    'Id selectionné':id,
    "Livre modifiéé": lc.format(),
    })

#########################################################################
#
#               Endpoint Methode permattant la modification de l'auteur du livre
#
#########################################################################
             

@app.route('/livres/auteur/<int:id>', methods=['PATCH'])
def modifier_auteur(id): 
    la=Livre.query.get(id)
    if la is None:
        abort(404)   
    else:  
        body = request.get_json()
        la.auteur = body.get('Nouvel auteur')                              
        la.update() 
    return jsonify({
    'Success': True,
    'Id selectionné':id,
    "Livre modifiéé": la.format(),
    }) 

#########################################################################
#
#               Endpoint Methode permattant la modification de l'éditeur du livre
#
#########################################################################
      
          
@app.route('/livres/editeur/<int:id>', methods=['PATCH'])
def modifier_editeur(id): 
    lv=Livre.query.get(id)
    if lv is None:
        abort(404)   
    else:  
        body = request.get_json()
        lv.editeur = body.get('Nouvel editeur')                              
        lv.update() 
    return jsonify({
    'Success': True,
    'Id selectionné':id,
    "Livre modifiéé": lv.format(),
    })   

#########################################################################
#
#               Endpoint Methode permattant la modification de la date de publication du livre
#
#########################################################################
      
@app.route('/livres/date/<int:id>', methods=['PATCH'])
def modifier_date(id): 
    lv=Livre.query.get(id)
    if lv is None:
        abort(404)   
    else:  
        body = request.get_json()
        lv.dat_publication = body.get('Nouvele date')                              
        lv.update() 
    return jsonify({
    'Success': True,
    'Id selectionné':id,
    "Livre modifiéé": lv.format(),
    })  
    
#########################################################################
#
#               Endpoint Gestion des erreurs
#
#########################################################################
     
     
# Erreur 404

@app.errorhandler(404)
def not_found(error):
    return jsonify({
    'Success': False,
    'error': 404,
    "Message":" Not found",           
     }), 404      
  
 
 # Erreur 500
    
@app.errorhandler(500)
def not_found(error):
    return jsonify({
    'Success': False,
    'error': 500,
    "Message":"Erreur interne au serveur",           
     }), 500 
    
       
# Erreur 400
   
@app.errorhandler(400)
def not_found(error):
    return jsonify({
    'Success': False,
    'error': 400,
    "Message":"Mauvaise requete",           
     }), 400
    
@app.errorhandler(405)
def not_found(error):
    return jsonify({
    'Success': False,
    'error': 405,
    "Message":"Mauvaise méthode",           
     }), 405            