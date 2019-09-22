# @Author: chunyang.xu
# @Email:  398745129@qq.com
# @Date:   2019-09-22 10:31:59
# @Last Modified time: 2019-09-22 12:41:32
# @github: https://github.com/longfengpili

#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import xlsxwriter
import numpy as np


class WriteDataToExcel(object):
	'''
	【Example】:
	datas = {'test' : [['a', 'b', 'c'], [1, 2, 3], [5, 6, 7]],
		    'test2' : [['a', 'b', 'c'], [1, 2, 3], [5, 6, 7]],
		    'test6' : [['a', 'b', 'c'], [1, 2, 3], [5, 6, 7]]}
	wdtexcel = WriteDataToExcel('./test.xlsx')
	wdtexcel.write_sheets(datas)
	wdtexcel.set_sheet_formula_conditional('test2', 'a1:c100', '=$b1="b"')
	wdtexcel._close()
	'''

	def __init__(self, filepath):
		self.filepath = filepath
		self.wb = xlsxwriter.Workbook(filepath)

	def add_sheet(self, sheetname):
		sheet = self.wb.add_worksheet(sheetname)
		return sheet

	def get_sheet(self, sheetname):
		sheet = self.wb.get_worksheet_by_name(sheetname)
		if not sheet:
			sheet = self.add_sheet(sheetname)
		return sheet

	def _close(self):
		self.wb.close()


	def set_coverformat(self,font_size=9, font_color='#000000', bordernum=1, font_name='微软雅黑'):
		'''
		设置封面单元格样式
		:param font_size: 字体大小，默认9
		:param bg_color: 背景颜色，默认白色
		:param font_color: 字体颜色，默认黑色
		:param bordernum: 边框，默认1-有边框
		:param font_name: 字体，默认微软雅黑
		:return: 单元格样式
		'''
		coverformat=self.wb.add_format({'align': 'center', 'valign': 'vcenter', 'border': bordernum, 
									'font_size': font_size, 'font_color': font_color, 'font_name': font_name})
		return coverformat

	def set_cellformat(self, font_size=9, font_color='#000000', bordernum=0, font_name='微软雅黑', text_wrap=0):
		'''
		设置单元格样式
		:param font_size: 字体大小，默认9
		:param bg_color: 背景颜色，默认白色
		:param font_color: 字体颜色，默认黑色
		:param bordernum: 边框，默认1-有边框
		:param font_name: 字体，默认微软雅黑
		:param text_wrap: 自动换行，默认0-不自动换行
		:return: 单元格样式
		'''
		cellformat=self.wb.add_format({'align': 'center', 'valign': 'vcenter', 'border': bordernum,
										'font_size': font_size, 'font_color': font_color, 
										'font_name': font_name, 'text_wrap': text_wrap})
		return cellformat

	def set_column_width(self, sheetname, rangecell, width):
		'''
		设置指定单元格的宽度
		:param sheetname: sheet名称
		:param rangecell: 单元格范围,例如'A1:A5',单个单元格就是'A1:A1'
		:param width: 宽度
		'''
		sheet = self.get_sheet(sheetname)
		sheet.set_column(rangecell, width)

	def set_row_height(self, sheetname, rowx, height):
		'''
		设置指定行的高度
		:param sheetname: sheet名称
		:param rowx: 行数（从0开始）
		:param height: 高度
		'''
		sheet = self.get_sheet(sheetname)
		sheet.set_row(rowx, height)

	def write_cell(self, sheetname, cell, data, cellformat=None):
		'''
		编辑指定sheet下的单元格
		:param sheetname: sheet名称
		:param cell: 单元格
		:param data: 写入数据
		:param cellformat: 单元格样式
		'''
		if not cellformat:
			cellformat = self.set_cellformat()

		sheet = self.get_sheet(sheetname)
		sheet.write(cell.upper(), data, cellformat)

	def write_merge_range(self, sheetname, rangecell, data, cellformat=None):
		'''
		合并单元格并写入数据
		:param sheetname: sheet名称
		:param rangecell: 合并单元格范围，例如'D1:D7'
		:param data: 写入数据信息
		:param format: 单元格样式
		'''
		if not cellformat:
			cellformat = self.set_cellformat()

		sheet = self.get_sheet(sheetname)
		sheet.merge_range(rangecell.upper(), data, format)

	def write_sheet(self, sheetname, header, data, cellformat=None):
		if not cellformat:
			cellformat = self.set_cellformat()

		sheet = self.get_sheet(sheetname)
		sheet.write_row(0, 0, header, cellformat)
		for id, value in enumerate(data):
			value = ['' if v is np.nan else v for v in value]
			row = id + 1
			sheet.write_row(row, 0, value, cellformat)

	def write_sheets(self, datas, cellformat=None):
		if not isinstance(datas, dict):
			raise """your datas must be a dict, 
					example: 
					{'sheetname1': [[header], [row1], [row2] ……], 
					'sheetname2': [[header], [row1], [row2] ……], 
					……}"""
		else:
			for sheetname in datas:
				header = datas.get(sheetname)[0]
				data = datas.get(sheetname)[1:]
				self.write_sheet(sheetname, header, data, cellformat)

	def set_sheet_formula_conditional(self, sheetname, rangecell, criteria):
		'''
		条件格式
		:param sheetname: sheet名称
		:param rangecell: 单元格范围，例如'A1:D7'
		:param criteria: 公式， 例如'=$f1="well"'
		'''
		sheet = self.get_sheet(sheetname)
		wb_format = self.wb.add_format({'bg_color': '#FFC7CE'})
		sheet.conditional_format(rangecell.upper(), {
	        'type': 'formula',
	        'criteria': criteria,
	        'format': wb_format})




