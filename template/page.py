#!/usr/bin/env python
# -*- coding: utf-8 -*-

from constant import Website, WEBSITE_NAME, AIRPORT_NAME

main_page1 = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
　<head>
　　<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
　　<title>机票信息</title>
    <style type="text/css">
        html, body, div, span, applet, object, iframe, h1, h2, h3, h4, h5, h6, p, blockquote, pre, a, abbr, acronym, address, big, cite, code, del, dfn, em, img, ins, kbd, q, s, samp, small, strike, strong, sub, sup, tt, var, b, u, i, center, dl, dt, dd, ol, ul, li, fieldset, form, label, legend, table, caption, tbody, tfoot, thead, tr, th, td, article, aside, canvas, details, embed, figure, figcaption, footer, header, hgroup, menu, nav, output, ruby, section, summary, time, mark, audio, video {
          margin: 0;
          padding: 0;
          border: 0;
          font-size: 100%;
          font: inherit;
          vertical-align: baseline;
          outline: none;
          -webkit-font-smoothing: antialiased;
          -webkit-text-size-adjust: 100%;
          -ms-text-size-adjust: 100%;
          -webkit-box-sizing: border-box;
          -moz-box-sizing: border-box;
          box-sizing: border-box;
        }
        html { overflow-y: scroll; }
        body {
          background: #eee url('http://i.imgur.com/eeQeRmk.png'); /* http://subtlepatterns.com/weave/ */
          font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
          font-size: 75%;
          line-height: 1;
          color: #585858;
          padding: 22px 10px;
          padding-bottom: 55px;
        }

        ::selection { background: #5f74a0; color: #fff; }
        ::-moz-selection { background: #5f74a0; color: #fff; }
        ::-webkit-selection { background: #5f74a0; color: #fff; }

        br { display: block; line-height: 1.6em; }

        article, aside, details, figcaption, figure, footer, header, hgroup, menu, nav, section { display: block; }
        ol, ul { list-style: none; }

        input, textarea {
          -webkit-font-smoothing: antialiased;
          -webkit-text-size-adjust: 100%;
          -ms-text-size-adjust: 100%;
          -webkit-box-sizing: border-box;
          -moz-box-sizing: border-box;
          box-sizing: border-box;
          outline: none;
        }

        blockquote, q { quotes: none; }
        blockquote:before, blockquote:after, q:before, q:after { content: ''; content: none; }
        strong, b { font-weight: bold; }

        table { border-collapse: collapse; border-spacing: 0; }
        img { border: 0; max-width: 100%; }

        h1 {
          font-family: 'Amarante', Tahoma, sans-serif;
          font-weight: bold;
          font-size: 2em;
          line-height: 1.7em;
          margin-bottom: 10px;
          text-align: center;
        }

        h3 {
          font-family: 'Amarante', Tahoma, sans-serif;
          font-weight: bold;
          font-size: 1.3em;
          line-height: 1em;
          margin-bottom: 10px;
          text-align: center;
        }

        /** page structure **/
        #wrapper {
          display: block;
          width: 850px;
          background: #fff;
          margin: 0 auto;
          padding: 10px 17px;
          -webkit-box-shadow: 2px 2px 3px -1px rgba(0,0,0,0.35);
        }

        #keywords {
          margin: 0 auto;
          font-size: 1.2em;
          margin-bottom: 15px;
        }


        #keywords thead {
          cursor: pointer;
          background: #c9dff0;
        }
        #keywords thead tr th {
          font-weight: bold;
          padding: 12px 30px;
          padding-left: 42px;
        }
        #keywords thead tr th span {
          padding-right: 20px;
          background-repeat: no-repeat;
          background-position: 100% 100%;
        }

        #keywords thead tr th.headerSortUp, #keywords thead tr th.headerSortDown {
          background: #acc8dd;
        }

        #keywords thead tr th.headerSortUp span {
          background-image: url('http://i.imgur.com/SP99ZPJ.png');
        }
        #keywords thead tr th.headerSortDown span {
          background-image: url('http://i.imgur.com/RkA9MBo.png');
        }


        #keywords tbody tr {
          color: #555;
        }
        #keywords tbody tr td {
          text-align: center;
          padding: 15px 10px;
        }
        #keywords tbody tr td.lalign {
          text-align: left;
        }
      </style>
　　<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
　</head>

<body>
 <div id="wrapper">'''

main_page2 = '''
 </div>
</body>
</html>'''

body = '''
     <div>
          <h1>%s</h1>

          <table id="keywords" cellspacing="0" cellpadding="0">
            <thead>
              <tr>
                <th><span>价格</span></th>
                <th><span>起</span></th>
                <th><span>落</span></th>
                <th><span>来源</span></th>
                <th><span>详细</span></th>
              </tr>
            </thead>
            <tbody>
              %s
            </tbody>
          </table>
          %s
         </div>
         '''

one_item = '''              <tr>
                <td>%s</td>
                <td>%s[%s]</td>
                <td>%s[%s]</td>
                <td>%s</td>
                <td>%s</td>
              </tr>'''

trend_info = """
          <h3>%s</h3>

          <table id="keywords" cellspacing="0" cellpadding="0">
            <thead>
              <tr>
                <th><span>价格</span></th>
                <th><span>抓取时间</span></th>
                <th><span>起落</span></th>
                <th><span>来源</span></th>
                <th><span>航班号</span></th>
              </tr>
            </thead>
            <tbody>
              %s
            </tbody>
          </table>
"""

trend_item = '''              <tr>
                <td>%s</td>
                <td>%s</td>
                <td>%s => %s</td>
                <td>%s</td>
                <td>%s</td>
              </tr>'''


def get_html(message_info, trend_dict):
    divs = []
    for message in message_info:
        all_items = []
        for flight in message['flights']:
            url_info = u'<a href="%s">%s</a>' % \
                       (str(flight['url']), WEBSITE_NAME[flight['website']])
            all_items.append(
                one_item % (u'¥'+str(flight['price']), flight['from_time'],
                            AIRPORT_NAME[flight['from_airport']],
                            flight['to_time'],
                            AIRPORT_NAME[flight['to_airport']], url_info,
                            flight['airline']+' '+flight['flight_no']))
        date_flights = trend_dict[(message['date'], message['from_city'],
                                   message['to_city'])]
        all_trend_items = []
        for k in ['all'] + Website.ALL:
            trend_flights = date_flights.get(k)
            if not trend_flights and len(trend_flights) > 0:
                continue
            tmp_items = []
            for tmp in trend_flights:
                tmp_items.append(
                    trend_item % (u'¥'+str(tmp['price']),
                                  tmp['fetch_time'],
                                  tmp['from_time'],
                                  tmp['to_time'],
                                  WEBSITE_NAME[tmp['website']],
                                  tmp['airline'] + ' ' + tmp['flight_no']))
            head = u'汇总价格趋势' if k == 'all' else WEBSITE_NAME[k] + u'价格趋势'
            all_trend_items.append(trend_info % (head, '\n'.join(tmp_items)))
        divs.append(body % (u'%s[%s] %s => %s的航班' %
                            (message['date'], message['week_day_info'],
                             message['from_city_name'],
                             message['to_city_name']),
                            '\n'.join(all_items), '\n'.join(all_trend_items)))
    return main_page1 + u'\n'.join(divs) + main_page2