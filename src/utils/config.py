class Config:
  model = 'all-MiniLM-L6-v2'
  label_keywords = {
    'drivers_licence': 'license driver DMV identification permission',
    'bank_statement': 'account balance transaction bank statement',
    'invoice': 'invoice payment due amount description total cost',
    'cv': 'skills experience resume education work history role',
  }
  threshold = 0.3