import tempfile
import unittest
from pathlib import Path
from datetime import date,timedelta
from forecast import moving_average,backtest,forecast,load


class ForecastTests(unittest.TestCase):
    def test_average(self):
        self.assertEqual(moving_average([1,2,3,4],2),3.5)
    def test_bad_window(self):
        with self.assertRaises(ValueError): moving_average([1],0)
    def test_insufficient_history(self):
        with self.assertRaises(ValueError): moving_average([1],2)
    def test_backtest(self):
        self.assertEqual(backtest([2,2,2,2],2)["mae"],0)
    def test_future_dates(self):
        series=[(date(2026,11,1)+timedelta(days=i),10) for i in range(4)]
        self.assertEqual(forecast(series,2,2)["forecast"][-1]["date"],"2026-11-06")
    def test_invalid_horizon(self):
        with self.assertRaises(ValueError): forecast([(date(2026,11,1),1)],1,0)
    def test_reject_negative(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/"data.csv"
            path.write_text("date,units\n2026-11-01,-2\n",encoding="utf-8")
            with self.assertRaises(ValueError): load(str(path))
    def test_load_and_sort(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/"data.csv"
            path.write_text("date,units\n2026-11-02,2\n2026-11-01,1\n",encoding="utf-8")
            self.assertEqual(load(str(path))[0][1],1)


if __name__=="__main__":
    unittest.main()
