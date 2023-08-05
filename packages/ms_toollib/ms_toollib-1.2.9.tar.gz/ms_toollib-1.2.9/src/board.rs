use ms_toollib::*;
use pyo3::prelude::*;

#[pyclass(name = "MinesweeperBoard")]
pub struct PyMinesweeperBoard {
    pub core: MinesweeperBoard,
}

#[pymethods]
impl PyMinesweeperBoard {
    #[new]
    pub fn new(board: Vec<Vec<i32>>) -> PyMinesweeperBoard {
        let c = MinesweeperBoard::new(board.clone());
        PyMinesweeperBoard {
            core: c,
        }
    }
    pub fn step(&mut self, e: &str, pos: (usize, usize)) {
        self.core.step(e, pos).unwrap();
    }
    pub fn step_flow(&mut self, operation: Vec<(&str, (usize, usize))>) {
        self.core.step_flow(operation).unwrap();
    }
    #[getter]
    fn get_game_board(&self) -> PyResult<Vec<Vec<i32>>> {
        Ok(self.core.game_board.clone())
    }
    #[getter]
    fn get_left(&self) -> PyResult<usize> {
        Ok(self.core.left)
    }
    #[getter]
    fn get_right(&self) -> PyResult<usize> {
        Ok(self.core.right)
    }
    #[getter]
    fn get_chording(&self) -> PyResult<usize> {
        Ok(self.core.chording)
    }
    #[getter]
    fn get_ces(&self) -> PyResult<usize> {
        Ok(self.core.ces)
    }
    #[getter]
    fn get_flag(&self) -> PyResult<usize> {
        Ok(self.core.flag)
    }
    #[getter]
    fn get_solved3BV(&self) -> PyResult<usize> {
        Ok(self.core.solved3BV)
    }
}

#[pyclass(name = "AvfVideo")]
pub struct PyAvfVideo {
    pub core: AvfVideo,
}

#[pymethods]
impl PyAvfVideo {
    #[new]
    pub fn new(file_name: &str) -> PyAvfVideo {
        let c = AvfVideo::new(file_name);
        PyAvfVideo {
            core: c,
        }
    }
    pub fn parse_video(&mut self) {
        self.core.parse_video().unwrap();
    }
    pub fn analyse(&mut self) {
        self.core.analyse();
    }
    pub fn analyse_for_features(&mut self, controller: Vec<&str>) {
        self.core.analyse_for_features(controller);
    }
}


