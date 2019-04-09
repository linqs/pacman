######################
# ANALYSIS QUESTIONS #
######################

# Change these default values to obtain the specified policies through
# value iteration.

def question2():
    """
    Description:
    [Enter a description of what you did here.]
    """

    answerDiscount = 0.9
    answerNoise = 0.2

    """ YOUR CODE HERE """

    """ END CODE """

    return answerDiscount, answerNoise

def question3a():
    """
    Description:
    [Enter a description of what you did here.]
    """

    answerDiscount = 0.9
    answerNoise = 0.2
    answerLivingReward = 0.0

    """ YOUR CODE HERE """

    """ END CODE """

    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3b():
    """
    Description:
    [Enter a description of what you did here.]
    """

    answerDiscount = 0.9
    answerNoise = 0.2
    answerLivingReward = 0.0

    """ YOUR CODE HERE """

    """ END CODE """

    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3c():
    """
    Description:
    [Enter a description of what you did here.]
    """

    answerDiscount = 0.9
    answerNoise = 0.2
    answerLivingReward = 0.0

    """ YOUR CODE HERE """

    """ END CODE """

    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3d():
    """
    Description:
    [Enter a description of what you did here.]
    """

    answerDiscount = 0.9
    answerNoise = 0.2
    answerLivingReward = 0.0

    """ YOUR CODE HERE """

    """ END CODE """

    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3e():
    """
    Description:
    [Enter a description of what you did here.]
    """

    answerDiscount = 0.9
    answerNoise = 0.2
    answerLivingReward = 0.0

    """ YOUR CODE HERE """

    """ END CODE """

    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question6():
    """
    Description:
    [Enter a description of what you did here.]
    """

    answerEpsilon = None
    answerLearningRate = None

    """ YOUR CODE HERE """

    """ END CODE """

    return answerEpsilon, answerLearningRate
    # If not possible, return 'NOT POSSIBLE'

if __name__ == '__main__':
    questions = [
        question2,
        question3a,
        question3b,
        question3c,
        question3d,
        question3e,
        question6,
    ]

    print('Answers to analysis questions:')
    for question in questions:
        response = question()
        print('    Question %-10s:\t%s' % (question.__name__, str(response)))
