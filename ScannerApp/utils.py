def validateBarcode(code,sampleType):
    "to validate a barcode if its right format"
    
    return len(code) == 10 and code.isnumeric()