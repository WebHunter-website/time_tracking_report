import csv
from datetime import datetime
from pprint import pprint
import pyperclip

EMAIL_CONTENT = '''
<div id="forwardbody1">
    <div style="font-size: 11pt; font-family: Arial,Helvetica,sans-serif;">
        <div id="v1v1forwardbody1">
            <div style="font-size: 11pt; font-family: Arial,Helvetica,sans-serif;">
                <div id="v1v1v1editbody1">
                    <div style="font-size: 11pt; font-family: Arial,Helvetica,sans-serif;">
                        <p>Dzień dobry,</p>
                        <p>Poniżej rozpiska dni przepracowanych w miesiącu {month} + faktury:</p>
                        <table style="border-collapse: collapse; width: 43.2942%; height: 156px;" border="1">
                            <tbody>
                                <tr style="height: 14px; background-color: black; color: white;">
                                    <td style="width: 7.15686%; height: 14px; text-align: center;">Tydzień</td>
                                    <td style="width: 3.43137%; height: 14px; text-align: center;">Przepracowanych dni
                                    </td>
                                    <td style="width: 4.11102%; height: 14px; text-align: center;">Suma brutto [PLN]
                                    </td>
                                </tr>
                                {report}
                            </tbody>
                        </table>
                        <div>&nbsp;</div>
                        <div>Suma dni: <span style="font-size: 14pt;"><strong>{suma_dni}</strong></span></div>
                        <div>Suma do wypłaty brutto: <span style="font-size: 14pt;"><strong>{do_wyplaty} zł</strong></span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
'''

MONTH_SHORT_MAP = {
    '01': 'STY',
    '02': 'LUT',
    '03': 'MAR',
    '04': 'KWI',
    '05': 'MAJ',
    '06': 'CZE',
    '07': 'LIP',
    '08': 'SIE',
    '09': 'WRZ',
    '10': 'PAŹ',
    '11': 'LIS',
    '12': 'GRU',
}
MONTH_LONG_MAP = {
    '-01-': 'Styczeń',
    '-02-': 'Luty',
    '-03-': 'Marzec',
    '-04-': 'Kwiecień',
    '-05-': 'Maj',
    '-06-': 'Czerwiec',
    '-07-': 'Lipiec',
    '-08-': 'Sierpień',
    '-09-': 'Wrzesień',
    '-10-': 'Październik',
    '-11-': 'Listopad',
    '-12-': 'Grudzień',
}

class Calendar():
    def __init__(self, file_name):
        self.file_name = input('Path to time report CSV file > ').replace('"', '')
        self.csv_content = self.get_content()

        self.date = datetime.now().date()
        self.month = '-' + f'0{self.date.month}'[-2:] + '-'

        self.split_csv_content_to_wheeks()
        self.wheeks_content = list(filter(self.filter_wheeks,self.wheeks_content))
        self.worktime_report_unformatted = self.worktime_report()
        self.worktime_report_formatted = self.format_worktime_report()

        pyperclip.copy(self.worktime_report_formatted)


    def get_content(self):
        with open(self.file_name, encoding='utf8') as file:
            content = csv.reader(file)
            content = list(content)[1:]
        return content

    def split_csv_content_to_wheeks(self):
        self.wheeks_content = list()
        for line in self.csv_content:
            if line[0] == 'niedziela':
                self.wheeks_content.append([])
            self.wheeks_content[-1].append(line)

    def filter_wheeks(self, wheek):
        dates = [day[1] for day in wheek]
        for date in dates:
            if self.month in date:
                return wheek
                
    def worktime_report(self):
        worktime_report_unformatted = list()
        for wheek in self.wheeks_content:
            wheek[1][4] = '0' if wheek[1][4] == '' else str(int(wheek[1][4]) / 8)[:1]
            worktime_report_unformatted.append(list((
                wheek[0][1],
                wheek[-1][1],
                wheek[1][4],
                wheek[1][7]
            )))
        return worktime_report_unformatted

    def format_worktime_report(self):
        worktime_report_formatted = list()
        suma_dni = 0
        do_wyplaty = 0

        for entry in self.worktime_report_unformatted:
            start_splitted = entry[0].split('-')
            end_splitted   = entry[1].split('-')
            start_month = MONTH_SHORT_MAP[start_splitted[1]]
            end_month   = MONTH_SHORT_MAP[end_splitted[1]]

            suma_dni   += int(entry[2])
            do_wyplaty += int(entry[3][:-3])

            worktime_report_formatted.append(
                f'''
                                <tr style="height: 38px;">
                                    <td style="width: 7.15686%; height: 38px; text-align: center;">
                                        <p>{start_month} {start_splitted[2]} - {end_month} {end_splitted[2]}</p>
                                    </td>
                                    <td style="width: 3.43137%; height: 38px; text-align: center;">{entry[2]}</td>
                                    <td style="width: 4.11102%; height: 38px; text-align: center;">{entry[3]}</td>
                                </tr>
                '''
            )

        return EMAIL_CONTENT.format(
            month = MONTH_LONG_MAP[self.month],
            report = ''.join(worktime_report_formatted),
            suma_dni = suma_dni,
            do_wyplaty = '{:,}'.format(do_wyplaty).replace(',', ' ')
        )

    def __str__(self):
        for wheek in self.wheeks_content:
            pprint(wheek)
        print('-'*40)
        for entry in self.worktime_report_unformatted:
            pprint(entry)
        print('-'*40)
        print(self.worktime_report_formatted)
        return ''

def main():
    calendar = Calendar(r'C:\Users\sg0310013\Desktop\tt.csv')
    print(calendar)

if __name__ == '__main__':
    main()