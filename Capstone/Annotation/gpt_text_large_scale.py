from openai import OpenAI
import openpyxl

path = "./all_text_ads.xlsx"

prompts = ["Assign one or more codes to the advertisements following the rules in the codebook. Please give each one as a list and only mention the codes that apply. Seperate the result of each as with =====."]

codebook = ""
with open("./codebook.txt", encoding='utf-8') as file:
    codebook = file.read()



i = 199
while i<1129:
    print("----------- "+str(i)+" -------------")

    wb = openpyxl.load_workbook(path)
    sheet_obj = wb.active
    text1 = sheet_obj.cell(row=i, column=2).value
    text2 = sheet_obj.cell(row=i+1, column=2).value
    text3 = sheet_obj.cell(row=i+2, column=2).value
    text4 = sheet_obj.cell(row=i+3, column=2).value
    text5 = sheet_obj.cell(row=i+4, column=2).value

    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text",
                     "text": "Codebook: " + codebook},
                    {
                        "type": "text",
                        "text": "Advertisement: " + text1,
                    },
                    {
                        "type": "text",
                        "text": "Advertisement: " + text2,
                    },
                    {
                        "type": "text",
                        "text": "Advertisement: " + text3,
                    },
                    {
                        "type": "text",
                        "text": "Advertisement: " + text4,
                    },
                    {
                        "type": "text",
                        "text": "Advertisement: " + text5,
                    },
                    {
                        "type": "text",
                        "text": prompts[0],
                    }
                ],
            },
        ],
    )

    print(response)

    responses = response.choices[0].message.content.strip().split("=====")
    print(len(responses))
    if len(responses) != 5:
        continue

    for text_response in responses:
        codes = ["E-2", "E-3", "E-4", "E-5", "E-6", "E-7", "E-8", "C-1", "C-2", "C-3", "C-4", "I-1", "I-2", "I-3", "I-4", "I-5", "I-6", "Ro-1:",
                 "Ro-7", "Ro-9", "Ro-10", "D-1", "D-2", "D-3", "D-4", "D-5", "D-6", "D-7", "D-8", "D-9", "D-10"]

        code_list = []
        for code in codes:
            if code in text_response:
                print("Code: " + code)
                if code == "Ro-1:":
                    code_list.append("Ro-1")
                else:
                    code_list.append(code)
        if code_list == []:
            code_list = "N"
        sheet_obj.cell(row=i, column=4).value = ','.join(code_list)
        sheet_obj.cell(row=i, column=5).value = response.choices[0].message.content.strip()

    wb.save(path)

    i += 5
