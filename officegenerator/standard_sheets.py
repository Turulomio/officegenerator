from logging import warning
from officegenerator.commons import Coord
from officegenerator.casts import lor_remove_columns, lor_remove_rows,  list_remove_positions

class Model:
    def __init__(self):
        self.hh=None
        self.vh=None

    def setTitle(self, title):
        self.title=title
        
    ## If you want only vertical headers you must add self.setHorizontalHeaders(None, sizes=10)
    ## @param hh List or NOne
    ## @param sizes int or List in cm, to generate document use, columnSizes_for_ods
    def setHorizontalHeaders(self, hh, sizes=10):
        self.hh=hh
        if hh==None:#Only vertical headers
            columns=100
        else:
            columns=len(self.hh)
        if sizes.__class__.__name__=="int":
            self.hh_sizes=[sizes]*columns
        else:
            self.hh_sizes=sizes
    
    ## @param hh List or NOne
    ## @param size int with the witdth in cm of the vertical header
    def setVerticalHeaders(self, vh, size=5):
        self.vh=vh
        self.vh_size=size
        
    ## Converts self.hh_sizes and self.hv_size in cm to ods sizes. It returns them together
    def columnSizes_for_ods(self):
        r=[]
        factor=30
        if self.vh is not None:
            r.append(self.vh_size*factor)
        for arg in self.hh_sizes:
                r.append(arg*factor)
        return r
        
    ## Converts self.hh_sizes in cm to xlsx sizes
    def columnSizes_for_xlsx(self):
        r=[]
        factor=6
        if self.vh is not None:
            r.append(self.vh_size*factor)
        for arg in self.hh_sizes:
                r.append(arg*factor)
        return r
        
    ## Converts self.hh_sizes in cm to odt sizes
    def columnSizes_for_odt(self):
        r=[]
        factor=30
        if self.vh is not None:
            r.append(self.vh_size*factor)
        for arg in self.hh_sizes:
                r.append(arg*factor)
        return r

    def setData(self, data):
        self.data=data
        
    ## Used to remove Columns in the self.data
    ## @param columnList List of integers with the column index to remove
    def removeColumns(self, columnList):
        if self.hh is not None:
            self.hh=list_remove_positions(self.hh, columnList)
        if self.data is not None:
            self.data=lor_remove_columns(self.data, columnList)
        else:
            warning("I can't remove columns if self.data is None")

    ## Used to remove Columns in the self.data
    ## @param columnList List of integers with the column index to remove
    def removeRows(self, rowList):
        if self.vh is not None:
            self.vh=list_remove_positions(self.vh, rowList)
        if self.data is not None:
            self.data=lor_remove_rows(self.data, rowList)
        else:
            warning("I can't remove rows if self.data is None")

    ## @param title String with the title of the sheet
    ## @param columns_title List of Strings
    ## @param data list of list
    ## @param sizes List of integers
    def xlsx_sheet(self, doc):
        doc.createSheet(self.title)
        doc.setColumnsWidth(self.columnSizes_for_xlsx())
        if self.hh is not None:
            doc.overwrite(self.__getFirstContentCoord().addRow(-1), [self.hh], doc.stOrange)
        if self.vh is not None:
            for i, header in enumerate(self.vh):
                doc.overwrite(self.__getFirstContentCoord().addColumn(-1).addRow(i), header, doc.stGreen, alignment="left")
        if self.__mustFillA1()==True:
            doc.overwrite("A1", " ",  doc.stOrange)

        for number, row in enumerate(self.data):
            for letter,  field in enumerate(row):
                doc.overwrite(self.__getFirstContentCoord().addRow(number).addColumn(letter), field)
        doc.freezeAndSelect(self.__getFirstContentCoord(), self.__getFirstContentCoord().addRow(number).addColumn(letter))

    ## @param title String with the title of the sheet
    ## @param columns_title List of Strings
    ## @param data list of list
    ## @param sizes List of integers
    def ods_sheet(self, doc):
        s=doc.createSheet(self.title)
        s.setColumnsWidth(self.columnSizes_for_ods())
        if self.hh is not None:
            s.add(self.__getFirstContentCoord().addRow(-1), [self.hh],  "OrangeCenter")
        if self.vh is not None :
            for i, header in enumerate(self.vh):
                s.add(self.__getFirstContentCoord().addColumn(-1).addRow(i), header, "GreenLeft")
        if self.__mustFillA1()==True:
            s.add("A1", "", "OrangeCenter")

        for number, row in enumerate(self.data):
            for letter,  field in enumerate(row):
                s.add(self.__getFirstContentCoord().addRow(number).addColumn(letter), field)
        s.freezeAndSelect(self.__getFirstContentCoord(),self.__getFirstContentCoord().addRow(number).addColumn(letter))

    def odt_table(self, doc, sizes, fontsize, after=True):
        return doc.table(self.hh, self.data, sizes, fontsize, self.title, after)        
        
    def __getFirstContentCoord(self):
        #firstcontentletter and firstcontentnumber
        if self.hh is None and self.vh is not None:
            return Coord("B1")
        elif self.hh is not None and self.vh is None:
            return Coord("A2")
        elif self.hh is not None and self.vh is not None:
            return Coord("B2")
        elif self.hh is None and self.vh is None:
            return Coord("A1")
        
    ## Return if A1 must be filled for a better view
    ## @param bool
    def __mustFillA1(self):
        if self.hh is not None and self.vh is not None:
            return True
        return False

if __name__ == "__main__":
    from officegenerator.libodfgenerator import  ODS_Write
    from officegenerator.libodfgenerator import ODT_Standard
    from officegenerator.libxlsxgenerator import OpenPyXL
    filename="standard_sheets.ods"
    ods=ODS_Write("standard_sheets.ods")
    odt=ODT_Standard("standard_sheets.odt")
    xlsx=OpenPyXL("standard_sheets.xlsx")
    
    m=Model()
    m.setTitle("Probe")
    m.setHorizontalHeaders(["Number", "Data", "More data"], [1, 2, 3])
    m.setVerticalHeaders(["Number", "Data", "More data"]*10, 4)
    data=[]        
    for row in range(30):
        data.append([row, "Data", "Data++"])
    m.setData(data)
    m.ods_sheet(ods)
    m.xlsx_sheet(xlsx)
    
    m2=Model()
    m2.setTitle("Probe 2")
    m2.setHorizontalHeaders(None, [1, 2, 3])
    m2.setVerticalHeaders(["Number", "Data", "More data"]*10)
    m2.setData(data)
    m2.removeColumns([1, 2, ])
    m2.removeRows([1, 2, ])
    m2.ods_sheet(ods)
    m2.xlsx_sheet(xlsx)
    
    m.odt_table(odt, [3]*3, 8)
    
    xlsx.remove_sheet_by_id(0)
    ods.save()
    xlsx.save()
    odt.save()
