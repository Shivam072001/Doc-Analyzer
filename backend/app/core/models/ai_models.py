from transformers import pipeline

class DocumentClassifier:
    """
    A module for classifying documents into predefined categories and subcategories
    using a user-specified pre-trained Hugging Face model.
    """

    def __init__(self, model_name):
        """
        Initializes the DocumentClassifier with a specified pre-trained model.

        Args:
            model_name (str): The name of the pre-trained Hugging Face
                model to use for text classification. This will be provided by the user.
        """
        try:
            self.classifier = pipeline("text-classification", model=model_name)
            self.category_map = self._build_category_map(self._get_classification_hierarchy())
        except Exception as e:
            raise ValueError(f"Error loading the specified model '{model_name}': {e}")

    def _get_classification_hierarchy(self):
        """
        Returns the predefined document classification hierarchy.

        Returns:
            dict: A dictionary representing the document classification hierarchy.
        """
        return {
            "DocumentClassification": {
                "Administrative Documents": {
                    "Policies & Procedures": [
                        "Company Policies",
                        "Standard Operating Procedures (SOPs)"
                    ],
                    "Reports & Audits": [
                        "Annual Reports",
                        "Financial Reports",
                        "Audit Reports"
                    ],
                    "Contracts & Agreements": [
                        "Employment Contracts",
                        "Vendor Agreements",
                        "Non-Disclosure Agreements (NDAs)"
                    ],
                    "Correspondence": [
                        "Internal Memos",
                        "Official Letters",
                        "Emails"
                    ]
                },
                "Financial Documents": {
                    "Accounting Records": [
                        "Balance Sheets",
                        "Income Statements",
                        "Cash Flow Statements"
                    ],
                    "Tax & Compliance": [
                        "Tax Returns",
                        "Audit Reports",
                        "Regulatory Filings"
                    ],
                    "Invoices & Payments": [
                        "Invoices",
                        "Receipts",
                        "Payment Confirmations"
                    ]
                },
                "Legal Documents": {
                    "Corporate Governance": [
                        "Articles of Incorporation",
                        "Board Meeting Minutes"
                    ],
                    "Intellectual Property (IP)": [
                        "Patents",
                        "Trademarks",
                        "Copyrights"
                    ],
                    "Litigation & Case Files": [
                        "Lawsuits",
                        "Court Orders"
                    ],
                    "Compliance & Regulations": [
                        "GDPR Compliance Documents",
                        "ISO Certifications"
                    ]
                },
                "Human Resources (HR) Documents": {
                    "Employee Records": [
                        "Resumes & Applications",
                        "Performance Reviews"
                    ],
                    "Payroll & Benefits": [
                        "Salary Slips",
                        "Benefits Enrollment Forms"
                    ],
                    "Training & Development": [
                        "Training Manuals",
                        "Certificates"
                    ]
                },
                "Technical & IT Documents": {
                    "Software Documentation": [
                        "APIs & SDKs",
                        "Source Code Repositories"
                    ],
                    "IT Policies & Security": [
                        "Data Privacy Policies",
                        "Cybersecurity Reports"
                    ],
                    "Infrastructure & Architecture": [
                        "Network Diagrams",
                        "Cloud Deployment Models"
                    ]
                },
                "Marketing & Sales Documents": {
                    "Marketing Materials": [
                        "Brochures",
                        "Social Media Content"
                    ],
                    "Sales Documents": [
                        "Proposals & Quotes",
                        "Customer Contracts"
                    ],
                    "Market Research & Analytics": [
                        "Competitor Analysis Reports",
                        "SEO Reports"
                    ]
                },
                "Product & Project Documents": {
                    "Product Development": [
                        "Requirement Specifications",
                        "Prototypes & Wireframes"
                    ],
                    "Project Management": [
                        "Project Plans",
                        "Risk Assessments"
                    ]
                },
                "Research & Academic Documents": {
                    "Research Papers": [
                        "White Papers",
                        "Case Studies"
                    ],
                    "Academic Records": [
                        "Theses & Dissertations",
                        "Course Syllabi"
                    ]
                },
                "Miscellaneous Documents": {
                    "General Reference": [
                        "FAQs",
                        "Glossaries"
                    ],
                    "Miscellaneous": [
                        "Press Releases",
                        "Event Agendas"
                    ]
                }
            }
        }

    def _build_category_map(self, hierarchy):
        """
        Builds a flattened map of all possible subcategories.

        Args:
            hierarchy (dict): The document classification hierarchy.

        Returns:
            dict: A dictionary where keys are subcategories and values are
                  tuples of (main_category, subcategory).
        """
        category_map = {}
        for main_category, sub_categories in hierarchy["DocumentClassification"].items():
            for sub_category, labels in sub_categories.items():
                for label in labels:
                    category_map[label] = (main_category, sub_category)
        return category_map

    def predict(self, document_text):
        """
        Predicts the category and subcategory of a given document text.

        Args:
            document_text (str): The text content of the document.

        Returns:
            dict: A dictionary containing the predicted 'main_category' and 'subcategory',
                  or None if no match is found.
        """
        try:
            prediction = self.classifier(document_text)[0]
            predicted_label = prediction['label']
            if predicted_label in self.category_map:
                main_category, subcategory = self.category_map[predicted_label]
                return {
                    "main_category": main_category,
                    "subcategory": subcategory
                }
            else:
                return None  # Or you could return a default "Unknown" category
        except Exception as e:
            print(f"Error during prediction: {e}")
            return None

# Example Usage (now requires specifying the model):
if __name__ == "__main__":
    try:
        classifier = DocumentClassifier(model_name="distilbert-base-uncased-finetuned-sst-2-english")
        document1 = "This document outlines the company's policy on employee conduct and ethics."
        prediction1 = classifier.predict(document1)
        print(f"Document 1 Prediction: {prediction1}")

        classifier2 = DocumentClassifier(model_name="bert-base-uncased") # This might not be directly suitable without fine-tuning
        document2 = "Attached is the financial report for the fiscal year ending December 31, 2024."
        prediction2 = classifier2.predict(document2)
        print(f"Document 2 Prediction: {prediction2}")

    except ValueError as ve:
        print(f"Error initializing classifier: {ve}")