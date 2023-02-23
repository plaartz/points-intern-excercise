import sys, csv


def load_csv(filename: str) -> list:
    """This method takes a filename as an argument and loads each row from a csv into a 
        list entry as a dictionary.

    Args:
        filename (str): csv file where the transactions are stored in the 
                        format payer (string), amount (integer), timestamp (date)

    Returns:
        list: A sorted list of dictionaries, where each dictionary is a row from the csv file 
            and sorted by timestamp
    """

    file_data = []
    with open(filename, newline='',encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row['points'] = int(row['points'])
            file_data.append(dict(row))
    file_data.sort(key=lambda date: date['timestamp'])
    return file_data


def spend(transactions: list, amount: int):
    """This method adjusts transaction amounts in the orginal list to adjust for the amount of 
        points the user is spending. If not enough points in transaction history, maintains 
        original list and raises an exception.

    Args:
        data (list): A list of dictionaries, where each dictionary contains data on a transaction, 
            including payer, amount, and timestamp
        amount (int): Amount of points to spend
    """

    temp_list = []
    for transaction in transactions:
        if transaction['points'] >= amount:
            transaction['points'] -= amount
            amount = 0
            break
        amount -= transaction['points']
        temp_list.append(transaction['points'])
        transaction['points'] = 0

    if amount > 0:
        for j, spend_history in enumerate(temp_list):
            transactions[j]['points'] = spend_history
        raise Exception("Not enough points")


def output(transactions: list) -> dict:
    """Returns a dictionary that contains all payer point balances given a list of transactions.

    Args:
        data (list): A data list that contains transaction history after spending points

    Returns:
        dict: A dictionary that contains all payer point balances
    """

    out = {}
    for entry in transactions:
        try:
            out[entry['payer']] += entry['points']
        except KeyError:
            out[entry['payer']] = entry['points']
    return out


if __name__ == "__main__":

    args = sys.argv[1:]
    try:
        if len(args) < 2:
            raise Exception('not enough arguments provided')

        data = load_csv(args[1])

        spend(data, int(args[0]))

        print(output(data))
    except Exception as e:
        print(str(e))
