from typing import List, Dict
from drug_mentions.models.schema import Drug, Publication, DrugMention

class DataTransformer:
    @staticmethod
    def find_drug_mentions(drugs: List[Drug], publications: List[Publication]) -> Dict[str, dict]:
        mentions = {}
        
        for drug in drugs:
            drug_mentions = {
                "mentions": {
                    "pubmed": [  
                        {
                            "id": pub.id,
                            "title": pub.title,
                            "date": pub.date.strftime('%Y-%m-%d'), 
                            "source": "pubmed"
                        }
                        for pub in publications 
                        if hasattr(pub, 'source') 
                        and pub.source == 'pubmed'
                        and drug.drug.lower() in pub.title.lower()
                    ],
                    "clinical_trials": [
                        {
                            "id": pub.id,
                            "title": pub.title,
                            "date": pub.date.strftime('%Y-%m-%d'),
                            "source": "clinical_trial"
                        }
                        for pub in publications
                        if hasattr(pub, 'source')
                        and pub.source == 'clinical_trial'
                        and drug.drug.lower() in pub.title.lower()
                    ],
                    "journals": [
                        {
                            "name": pub.journal,
                            "date": pub.date.strftime('%Y-%m-%d')
                        }
                        for pub in publications
                        if drug.drug.lower() in pub.title.lower()
                        and pub.journal is not None
                    ]
                }
            }
            
            # Only add drugs that have mentions
            if any(len(mentions) > 0 for mentions in drug_mentions["mentions"].values()):
                mentions[drug.drug] = drug_mentions
        
        return mentions