"""Sample request for extracting GraphQL part data."""
import argparse
import json

import requests

from nexar_token import get_token

NEXAR_URL = "https://api.nexar.com/graphql"
QUERY_MPN = """query ($mpn: String!) {
      supSearchMpn(q: $mpn) {
        results {
          part {
            category {
              parentId
              id
              name
              path
            }
            mpn
            manufacturer {
              name
            }
            shortDescription
            descriptions {
              text
              creditString
            }
            specs {
              attribute {
                name
                shortname
              }
              displayValue
            }
          }
        }
      }
    }
"""


def get_part_info_from_mpn(variables, token) -> dict:
    """Return Nexar response for the given mpn."""
    try:
        r = requests.post(
            NEXAR_URL,
            json={"query": QUERY_MPN, "variables": variables},
            headers={"token": token},
        )

        data = json.loads(r.text)["data"]["supSearchMpn"]
    except Exception:
        raise Exception("Error while getting Nexar response")
    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("client_id", help="The client ID.", type=str)
    parser.add_argument("client_secret", help="The client secret.", type=str)
    parser.add_argument("mpn", help="The mpn for the part request.", type=str)
    args = parser.parse_args()

    variables = {"mpn": args.mpn}
    token = get_token(args.client_id, args.client_secret)
    response = get_part_info_from_mpn(variables, token["access_token"])
    print(response)
