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
