"""
Export job data to Excel (XLSX) format
"""

import os
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment
from config import EXCEL_COLUMNS, COLUMN_WIDTHS, HEADER_COLOR, LINK_COLOR


def export_to_excel(jobs_data, output_filename=None):
    """
    Export job data to Excel file

    Args:
        jobs_data: List of job dictionaries
        output_filename: Optional custom filename

    Returns:
        Filepath of created Excel file
    """
    if output_filename is None:
        today = datetime.now().strftime("%Y-%m-%d")
        output_filename = f"UK_jobs_{today}.xlsx"

    # Ensure output directory exists
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_path = os.path.join(output_dir, output_filename)

    # Create workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Job Listings"

    # Write header
    for col_num, column_title in enumerate(EXCEL_COLUMNS, 1):
        cell = ws.cell(row=1, column=col_num)
        cell.value = column_title

        # Header styling
        header_fill = PatternFill(start_color=HEADER_COLOR, end_color=HEADER_COLOR, fill_type="solid")
        header_font = Font(name="Arial", size=10, bold=True)
        header_alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = header_alignment

    # Set column widths
    for col_letter, width in COLUMN_WIDTHS.items():
        ws.column_dimensions[col_letter].width = width

    # Write data rows
    for row_num, job in enumerate(jobs_data, 2):
        # 更新时间 (Update date)
        ws.cell(row=row_num, column=1).value = job.get("update_date", datetime.now().strftime("%Y-%m-%d"))

        # 公司名称 (Company)
        ws.cell(row=row_num, column=2).value = job.get("company", "")

        # 项目类型 (Project type)
        ws.cell(row=row_num, column=3).value = job.get("project_type", "")

        # 闭岗时间 (Closed date) - LinkedIn doesn't provide this
        ws.cell(row=row_num, column=4).value = "/"

        # 项目时间 (Project duration) - LinkedIn doesn't provide this
        ws.cell(row=row_num, column=5).value = "/"

        # 岗位类型 (Job type)
        ws.cell(row=row_num, column=6).value = job.get("job_type", "")

        # 岗位名称 (Job title)
        ws.cell(row=row_num, column=7).value = job.get("title", "")

        # 工作地区 (Location)
        ws.cell(row=row_num, column=8).value = job.get("location", "")

        # 学历要求 (Education requirement)
        ws.cell(row=row_num, column=9).value = job.get("education", "官网无说明")

        # 毕业时间 (Graduation date)
        ws.cell(row=row_num, column=10).value = "/"

        # Link
        link_cell = ws.cell(row=row_num, column=11)
        link_url = job.get("link", "")
        if link_url:
            link_cell.value = link_url
            link_cell.hyperlink = link_url
            link_font = Font(name="Arial", size=10, color=LINK_COLOR, underline="single")
            link_cell.font = link_font
        else:
            link_cell.value = ""

        # Data row styling
        data_font = Font(name="Arial", size=10)
        data_alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)

        for col_num in range(1, len(EXCEL_COLUMNS) + 1):
            cell = ws.cell(row=row_num, column=col_num)
            cell.font = data_font
            cell.alignment = data_alignment

    # Freeze header row
    ws.freeze_panes = "A2"

    # Save workbook
    wb.save(output_path)

    return output_path


def get_output_filename(custom_name=None):
    """
    Generate output filename

    Args:
        custom_name: Optional custom filename

    Returns:
        Filename string
    """
    if custom_name:
        return custom_name

    today = datetime.now().strftime("%Y-%m-%d")
    return f"UK_jobs_{today}.xlsx"
