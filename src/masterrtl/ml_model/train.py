import xgboost as xgb


def train(x_train, y_train):
    xgbr = xgb.XGBRegressor(n_estimators=25, max_depth=12, nthread=20)
    xgbr.fit(x_train, y_train)

    return xgbr
