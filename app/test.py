from app.models.auditeur import Auditeur
from app.models.affect import Affect
from app.core.database import SessionLocal
from app.models.ip import IP
from app.models.prestataire import Prestataire
from app.models.audit import Audit

db = SessionLocal()

# Récupérer un auditeur et une affectation existante
auditeur = db.query(Auditeur).first()
affect = db.query(Affect).first()
prestataire = db.query(Prestataire).first()
audit = db.query(Audit).first()
ip= db.query(IP).first()

if auditeur and affect:
    print(f"Affectation ID: {affect.id}, Auditeur ID: {auditeur.id}")

    # Ajouter l'auditeur à l'affectation
    affect.auditeurs.append(auditeur)
    db.commit()

    print("Liaison ajoutée avec succès !")
else:
    print("Aucun auditeur ou affect trouvé")
