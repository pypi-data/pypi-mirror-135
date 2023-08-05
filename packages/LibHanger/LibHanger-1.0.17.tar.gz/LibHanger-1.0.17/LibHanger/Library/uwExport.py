import pandas as pd

class BaseExport():
    
    """
    エクスポートクラス基底
    """
    
    pass

class BaseImport():

    """
    インポートクラス基底
    """

    pass

class ExcelImporter(BaseImport):

    """
    Excelインポートクラス
    """
    
    def __init__(self):
        
        """
        コンストラクタ
        
        Parameters
        ----------
        None
        
        """
        
        self.workbooks = None
        """Excelワークブック"""

        self.sheets = None
        """Excelワークシート"""

        self.filepath = None
        """Excelファイルパス"""
        
    def openBook(self, filePath:str):
        
        """
        Excelブックを開く
        
        Parameters
        ----------
        filePath : str
            ファイルパス
            
        """
        
        # ファイルパス保持
        self.filepath = filePath
        # ブックの読み込み
        self.workbooks = pd.ExcelFile(filePath)
        # シートの読み込み
        self.sheets = self.workbooks.sheet_names
        
class ExcelExporter(BaseExport):
    
    """
    Excelエクスポートクラス
    """
    
    pass
