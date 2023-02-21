import sys, csv

def load_csv(filename: str) -> list:
    """This method takes a filename as an argument and loads each row from a csv into a list entry as a dictionary.

    Args:
        filename (str): csv file where the transactions are stored in the 
                        format payer (string), amount (integer), timestamp (date)

    Returns:
        list: A sorted list of dictionaries, where each dictionary is a row from the csv file and sorted by timestamp
    """

    data = []
    with open(filename, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['points'] = int(row['points'])
            data.append(row)
    data.sort(key=lambda date: date['timestamp'])
    return data


def spend(data: list, amount: int):
    """This method adjusts transaction amounts in the orginal list to adjust for the amount of points the user is spending. If not enough
        points in transaction history, maintains original list and raises an exception.

    Args:
        data (list): A list of dictionaries, where each dictionary contains data on a transaction, including payer, amount, and timestamp
        amount (int): Amount of points to spend
    """
    
    tempList = []
    for i in range(len(data)):
        if data[i]['points'] >= amount:
            data[i]['points'] -= amount
            amount = 0
            break
        else:
            amount -= data[i]['points']
            tempList.append(data[i]['points'])
            data[i]['points'] = 0
            
    if amount > 0:
        for j in range(len(tempList)):
            data[j]['points'] = tempList[j]
        raise Exception("Not enough points")
    
    
def output(data: list) -> dict:
    """Returns a dictionary that contains all payer point balances given a list of transactions.

    Args:
        data (list): A data list that contains transaction history after spending points

    Returns:
        dict: A dictionary that contains all payer point balances
    """

    out = {}
    for entry in data:
        try:
            out[entry['payer']] += entry['points']
        except KeyError:
            out[entry['payer']] = entry['points']
    return out


if __name__ == "__main__":

    args = sys.argv[1:]
    try:
        if (len(args) < 2):
            raise Exception('not enough arguments provided')

        data = load_csv(args[1])
        
        spend(data, int(args[0]))
        
        print(output(data))
    except Exception as e:
        print(str(e))
