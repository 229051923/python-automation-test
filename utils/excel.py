# -*- coding: utf-8 -*-
import os
import pandas as pd


class ParseExcel(object):
    """
    解析Excel
    """

    def __init__(self, file_name):
        self.file = file_name
        if os.path.exists(file_name):
            try:
                self.excel = pd.ExcelFile(file_name)
            except Exception as e:
                pass
            finally:
                if self.excel:
                    self.excel.close()
        else:
            raise FileNotFoundError(f"{file_name}文件不存在")

    @property
    def sheet_names(self):
        """
        获取sheet名字
        :return:
        """
        return self.excel.sheet_names

    def get_data(self, sheet_name=None) -> list:
        """
        获取excel所有行 返回list
        :param sheet_name:
        :return:
        """
        if not sheet_name:
            sheet_name = self.excel.sheet_names[0]
        data_frame = self.excel.parse(sheet_name, na_values=['NA'], header=None)
        data_frame = data_frame.replace(pd.np.nan, '', regex=True)
        data = data_frame.get_values().tolist()
        return data

    def get_head(self, sheet_name=None) -> list:
        """
        获取表头，默认是第一行数据
        :param sheet_name:
        :return:
        """
        if not sheet_name:
            sheet_name = self.excel.sheet_names[0]
        headers = list(self.excel.parse(sheet_name, nrows=1).columns)
        return headers

    def filter_data(self, sheet_name=None, col=0, value=None):
        """
        筛选数据
        :param sheet_name:
        :param col: 列序列号，从0开始
        :param value:列值
        :return:
        """
        if not sheet_name:
            sheet_name = self.excel.sheet_names[0]
        data_frame = self.excel.parse(sheet_name, na_values=['NA'], header=None)
        data_frame = data_frame.loc[data_frame[col] == value]
        data_frame = data_frame.replace(pd.np.nan, '', regex=True)
        data = data_frame.get_values().tolist()
        return data


def write_excel(file, data_list: list, sheet_name='sheet1', start_col=0, start_row=0):
    """
    :param file: 文件名
    :param data_list: 数据二维数组如 按行[[1, 2, 3, 4], [5, 6, 7, 8]]
    :param sheet_name: 页名字
    :param start_col: 开始列的位置
    :param start_row: 开始行的位置
    """
    df = pd.DataFrame(data_list)
    with pd.ExcelWriter(file) as w:
        df.to_excel(w, startcol=start_col, startrow=start_row, sheet_name=sheet_name,
                    header=False, index=False)


if __name__ == '__main__':
    # file = "C:\easytest-log\库龄数据.xlsx"
    # p = ParseExcel(file)
    # print(p.get_data())
    # print(p.get_head())
    # print(p.filter_data(col=3, value='N21226-c04879728ac74705adf6b8f09f261172'))
    a = [[1, 2, 3, 4], [5, 6, 7, 8]]
    write_excel("the_file.xlsx", a)
