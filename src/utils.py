def validate_input_user(data):
    test_value = []
    errors = []
    
    # EXPECTED_FEATURES = ("Alcohol", "Malic acid", "Ash", "Alcalinity of ash",
    #                      "Magnesium", "Total phenols", "Flavanoids", "Nonflavanoid phenols",
    #                      "Proanthocyanins", "Color intensity", "Hue",
    #                      "OD280/OD315 of diluted wines", "Proline")
    EXPECTED_FEATURES = ("user_id")
    
    if not data:
        errors.append("Form data must not be empty")
    else:
        for feature in EXPECTED_FEATURES:
            if feature not in data:
                errors.append(f"'{feature}' is a required field") 
            else:
                try:
                    test_value.append(float(data[feature]))
                except ValueError:
                    errors.append(f"Invalid value for field {feature}: '{data[feature]}'")

    return test_value, errors


def validate_input_wine(data):
    test_value = []
    errors = []
    
    # EXPECTED_FEATURES = ("Alcohol", "Malic acid", "Ash", "Alcalinity of ash",
    #                      "Magnesium", "Total phenols", "Flavanoids", "Nonflavanoid phenols",
    #                      "Proanthocyanins", "Color intensity", "Hue",
    #                      "OD280/OD315 of diluted wines", "Proline")
    EXPECTED_FEATURES = ("wine_id")
    
    if not data:
        errors.append("Form data must not be empty")
    else:
        for feature in EXPECTED_FEATURES:
            if feature not in data:
                errors.append(f"'{feature}' is a required field") 
            else:
                try:
                    test_value.append(float(data[feature]))
                except ValueError:
                    errors.append(f"Invalid value for field {feature}: '{data[feature]}'")

    return test_value, errors

    
