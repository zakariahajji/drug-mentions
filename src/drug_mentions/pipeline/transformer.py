from typing import List, Dict
from drug_mentions.models.schema import Drug, Publication, DrugMention

class DataTransformer:
    @staticmethod
    def find_drug_mentions(drugs: List[Drug], publications: List[Publication]) -> Dict[str, dict]:
        mentions = {}
        
        for drug in drugs:
            drug_mentions = {
                "pubmed_mentions": [],
                "clinical_trials_mentions": [],
                "journals": set()
            }
            
            for pub in publications:
                if drug.drug.lower() in pub.title.lower():
                    mention = {
                        "id": pub.id,
                        "title": pub.title,
                        "date": pub.date.strftime('%d/%m/%Y'),
                        "journal": pub.journal
                    }
                    
                    if hasattr(pub, 'source'):
                        if pub.source == 'pubmed':
                            drug_mentions["pubmed_mentions"].append(mention)
                        else:
                            drug_mentions["clinical_trials_mentions"].append(mention)
                    else:
                        # Default to pubmed if source not specified
                        drug_mentions["pubmed_mentions"].append(mention)
                    
                    drug_mentions["journals"].add(pub.journal)
            
            # Only add drugs that have mentions
            if drug_mentions["pubmed_mentions"] or drug_mentions["clinical_trials_mentions"]:
                drug_mentions["journals"] = list(drug_mentions["journals"])
                mentions[drug.drug] = drug_mentions
        
        return mentions