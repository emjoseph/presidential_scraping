import json
with open('nixon_remarks_w_toxicity.json') as remarks_file:
    remarks = json.load(remarks_file)
    true_remarks = []

    print(f'{len(remarks)} remarks...')

    for i in range(len(remarks)):
        remark = remarks[i]
        remark_title = remark['title']
        if remark_title.find("Remarks") > 0:
            true_remarks.append(remark)

    with open('nixon_remarks_true.json', 'w') as true_file:
        json.dump(true_remarks, true_file, indent=4, ensure_ascii=True)
