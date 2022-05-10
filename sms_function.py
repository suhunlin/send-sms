import os
from twilio.rest import Client

def read_file(filename):
    sms_read_format = []
    try:
        with open(filename,'r',encoding='utf-8-sig') as file:
            for line in file:
                sms_read_format.append(line.strip())
    except Exception as error_message:
        print(error_message)

    return sms_read_format

def handle_decoding_message(sms_read_format):
    sms_decoding = []
    str = ''

    if not sms_read_format:
        print('請傳送正確的檔案資料!!!')
    else:
        for sms_format in  sms_read_format:
            split_sms_read_format_by_blank = sms_format.split()#把訊息按照空白來切割
            if(len(split_sms_read_format_by_blank)) > 2:#讀取到的格式應該只有電話跟訊息兩塊，如果split後的訊息大於1表示訊息需要重新被處理成一塊訊息
                for word in split_sms_read_format_by_blank[1:]:
                    str += word + ' '#把讀出的訊息暫存加上空白鍵(英文間隔)存到str
                    split_sms_read_format_by_blank.pop(1)#pop掉第一個位置的訊息，讓後面的訊息往前移動
                split_sms_read_format_by_blank.append(str)#把處理好的訊息存回split_sms_read_format_by_blank
                str = ''
                sms_decoding.append(split_sms_read_format_by_blank)
            else:
                sms_decoding.append(split_sms_read_format_by_blank)
    return sms_decoding

def send_sms(sid,token,phone_number,sms_decoding):
    account_sid = sid
    accound_token = token
    if account_sid == None:
        print('Please input the correct account sid!!!')
        return
    elif accound_token == None:
        print('Please input the correct account token!!!')
        return
    elif phone_number == None:
        print('Please input the correct phone number!!!')
        return
    client = Client(account_sid,accound_token)
    for sms in sms_decoding:
        message = client.messages.create(
            to = sms[0],
            from_= phone_number,
            body = sms[1]
        )
        print(message.sid) #如果簡訊寄出成功，印出message的sid

def main():
    filename = 'sms.txt'
    sid = None # input your sid from twilio web
    token = None # input your token from twilio web
    my_pyhon = None #input your phone number from twilio web
    if os.path.exists(filename):
        sms_read_format = read_file(filename)
        sms_decoding = handle_decoding_message(sms_read_format)
        send_sms(sid,token,my_pyhon,sms_decoding)
    else:
        print('請輸入正確的檔案及路徑!!!')

if __name__ == '__main__':
    main()
