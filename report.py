# Copyright 2020
#
# Created by nguyenvantam at 7/14/21
# Modified by nguyenvantam
#
# -*- coding: utf-8 -*-
import xlsxwriter


class Report:
    def __init__(self):
        self.workbook = None

    def open(self, name):
        if 'xlsx' not in name: name += '.xlsx'
        self.workbook = xlsxwriter.Workbook(name)

    def close(self):
        self.workbook.close()

    def write_duration(self, duration_info):
        longs, mediums, shorts = duration_info
        worksheet = self.workbook.add_worksheet('duration')
        worksheet.write('A1', 'Number of long videos (more than 1h)')
        worksheet.write('B1', 'Number of medium videos (0.5h to 1h)')
        worksheet.write('C1', 'Number of short videos (less than 0.5h)')

        worksheet.write('A2', str(longs))
        worksheet.write('B2', str(mediums))
        worksheet.write('C2', str(shorts))

        chart = self.workbook.add_chart({'type': 'pie'})
        chart.add_series({
            'name': 'Video duration',
            'categories': ['duration', 0, 0, 0, 2],
            'values': ['duration', 1, 0, 1, 2],
        })

        worksheet.insert_chart('B5', chart)

    def write_summary_tag_analysis(self, summary):
        def get_item(group_id, all_items):
            for item in all_items:
                if item['_id'] == group_id:
                    return item

        worksheet = self.workbook.add_worksheet('summary_tags')
        worksheet.write('B1', 'Number of videos')
        for i in range(1, len(summary) + 1):
            worksheet.write(f'A{i + 1}', f'Group tag {i}')
            worksheet.write(f'B{i + 1}', str(get_item(i - 1, summary)['count']))

        chart = self.workbook.add_chart({'type': 'pie'})
        chart.add_series({
            'name': 'Video tags',
            'categories': ['summary_tags', 1, 0, len(summary), 0],
            'values': ['summary_tags', 1, 1, len(summary), 1],
        })

        worksheet.insert_chart('B5', chart)

    def write_detail_tag_analysis(self, detail):
        def get_item(group_id, all_items):
            for item in all_items:
                if item['_id'] == group_id:
                    return item

        worksheet = self.workbook.add_worksheet('detail_group_tags')
        worksheet.write('A1', 'Group tag')
        worksheet.write('B1', 'Video title')
        worksheet.write('C1', 'Video tags')
        row = 1
        for i in range(1, len(detail) + 1):
            row += 1
            worksheet.write(f'A{row}', f'Group tag {i}')
            item = get_item(i - 1, detail)
            for j in range(0, len(item['video_titles'])):
                worksheet.write(f'B{row}', item['video_titles'][j])
                worksheet.write(f'C{row}', ','.join(item['video_tags'][j] if len(item['video_tags']) > j else ''))
                row += 1

    def write_classify_tag_analysis(self, videos):
        worksheet = self.workbook.add_worksheet('classify_tags')
        worksheet.write('A1', 'Video title')
        worksheet.write('B1', 'Video tags')
        worksheet.write('C1', 'Class')
        row = 1
        for i in range(1, len(videos) + 1):
            row += 1
            worksheet.write(f'A{row}', videos[i - 1].get('title', ''))
            worksheet.write(f'B{row}', ','.join(videos[i - 1].get('tags', [])))
            worksheet.write(f'C{row}', ','.join(videos[i - 1].get('classes', [])))


report = Report()
