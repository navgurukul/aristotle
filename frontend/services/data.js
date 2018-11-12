export const getStages = () => {
  return {
    "stages": [
      {
        'order': 1,
        'totalLevels': 20,
        'currentLevel': 2,
        'name': 'Booleans',
        'id': 'booleans'
      },
      {
        'order': 2,
        'totalLevels': 25,
        'currentLevel': 5,
        'name': 'If Conditions',
        'id': 'if-conditions'
      },
      {
        'order': 3,
        'totalLevels': 25,
        'currentLevel': 5,
        'name': 'Modulous',
        'id': 'mod'
      },
      {
        'order': 4,
        'totalLevels': 25,
        'currentLevel': 5,
        'name': 'Math Operators',
        'id': 'math-op'
      },
      {
        'order': 5,
        'totalLevels': 25,
        'currentLevel': 5,
        'name': 'If/Else in Depth',
        'id': 'if-else-depth'
      },
      {
        'order': 6,
        'totalLevels': 25,
        'currentLevel': 5,
        'name': 'While Loops',
        'id': 'while-loops'
      },
      {
        'order': 7,
        'totalLevels': 25,
        'currentLevel': 5,
        'name': 'For Loops',
        'id': 'for-loops'
      },
      {
        'order': 8,
        'totalLevels': 25,
        'currentLevel': 5,
        'name': 'Functions',
        'id': 'functions'
      }
    ]
  }
}

export const getStageById = (id) => {
  let stage = null;
  let allStages = getStages().stages;
  for(let i=0;i<=allStages.length;i++){
    if(allStages[i]['id'] == id){
      stage = allStages[i];
      break;
    }
  }
  return stage;
}

export const getQuestions = (level, stageId) => {
  return {
    "questions": [
      {
        "text": "This is some text for the 1st question.",
        "answer": "answer1",
      },
      {
        "text": "This is some text for the 2nd question.",
        "answer": "answer2",
      },
      {
        "text": "This is some text for the 3rd question.",
        "answer": "answer3",
      },
      {
        "text": "This is some text for the 4th question.",
        "answer": "answer4",
      },
      {
        "text": "This is some text for the 5th question.",
        "answer": "answer5",
      },
      {
        "text": "This is some text for the 6th question.",
        "answer": "answer6",
      },
      {
        "text": "This is some text for the 7th question.",
        "answer": "answer7",
      },
      {
        "text": "This is some text for the 8th question.",
        "answer": "answer8",
      },
      {
        "text": "This is some text for the 9th question.",
        "answer": "answer9",
      },
      {
        "text": "This is some text for the 10th question.",
        "answer": "answer10",
      },
      {
        "text": "This is some text for the 11th question.",
        "answer": "answer11",
      },
      {
        "text": "This is some text for the 12th question.",
        "answer": "answer12",
      },
      {
        "text": "This is some text for the 13th question.",
        "answer": "answer13",
      },
      {
        "text": "This is some text for the 14th question.",
        "answer": "answer14",
      }
    ]
  }
}

export const clearLevel = (level, stageId) => {
  let key = "clearedLevels:"+stageId;
  let clearedLevels = localStorage.getItem(key);
  if(clearedLevels != null) {
    clearedLevels = JSON.parse(clearedLevels);
    clearedLevels = new Set(clearedLevels);
    clearedLevels.add(level);
    clearedLevels = Array.from(clearedLevels);
  } else {
    clearedLevels = [level]
  }
  localStorage.setItem(key, JSON.stringify(clearedLevels));
}

export const isLevelClear = (level, stageId) => {
  level = String(level);
  let key = "clearedLevels:"+stageId;
  let clearedLevels = localStorage.getItem(key);
  if (clearedLevels == null){
    return false
  } else {
    clearedLevels = JSON.parse(clearedLevels);
    let result = clearedLevels.indexOf(level) > -1 ? true : false;
    return result;
  }
}

export const getAllClearedLevels = (stageId) => {
  let key = "clearedLevels:"+stageId;
  let clearedLevels = localStorage.getItem(key);
  clearedLevels = clearedLevels == null ? [] : JSON.parse(clearedLevels);
  return clearedLevels;
}
