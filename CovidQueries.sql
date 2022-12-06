SELECT * 
FROM PortfolioProject.dbo.CovidDeaths
ORDER BY 3,4

-- Select Data that we are going to be using

SELECT location, date, total_cases, new_cases, total_deaths, population
FROM PortfolioProject.dbo.CovidDeaths
ORDER BY 1,2

-- Looking at Total Cases vs Total Deaths
-- Shows likelihood of dying if you contract covid in your country
SELECT location, date, total_cases, total_deaths, (total_deaths/total_cases)*100 AS DeathPercentage 
FROM PortfolioProject.dbo.CovidDeaths
WHERE location LIKE '%states%'
ORDER BY 1,2

-- Looking at Total cases vs Population

SELECT location, date, population, total_cases, (total_cases/population)*100 AS PercentPopulationInfected
FROM PortfolioProject.dbo.CovidDeaths
WHERE location LIKE '%states%'
ORDER BY 1,2

-- Looking at Countries with Highest Infection Rate compared to Population

SELECT location, population, MAX(total_cases) AS HighestInfectionCount, MAX((total_cases/population))*100 AS PercentPopulationInfected
FROM PortfolioProject.dbo.CovidDeaths
--WHERE location LIKE '%states%'
GROUP BY location, population
ORDER BY PercentPopulationInfected DESC

-- Showing Countries with Highest Death Count per Population

SELECT location, MAX(cast(total_deaths AS bigint)) AS TotalDeathCount
FROM PortfolioProject.dbo.CovidDeaths
--WHERE location LIKE '%states%'
WHERE continent IS NOT NULL
GROUP BY location
ORDER BY TotalDeathCount DESC

-- Breaking things down by Continent

SELECT location, MAX(cast(total_deaths AS bigint)) AS TotalDeathCount
FROM PortfolioProject.dbo.CovidDeaths
--WHERE location LIKE '%states%'
WHERE continent IS NULL
GROUP BY location
ORDER BY TotalDeathCount DESC

-- Global Numbers

SELECT SUM(new_cases) AS Total_Cases, SUM(cast(new_deaths as int)) AS Total_Deaths, 
	SUM(cast(new_deaths as int))/SUM(new_cases)*100 as DeathPercentage
FROM PortfolioProject.dbo.CovidDeaths
WHERE continent IS NOT NULL
ORDER BY 1,2


-- Looking at Total Population vs Vaccinations

SELECT dea.continent, dea.location, dea.date, dea.population, dea.new_vaccinations,
	SUM(cast(vac.new_vaccinations AS int)) OVER (PARTITION BY dea.location ORDER BY dea.location, dea.date) as RollingVaccinationCount
FROM PortfolioProject..CovidDeaths dea
JOIN PortfolioProject..CovidVaccinations vac
	ON dea.location = vac.location
	AND dea.date = vac.date
WHERE dea.continent IS NOT NULL
ORDER BY 2,3


-- CTE

WITH PopvsVac (continent, location, date, population, new_vaccinations, RollingVaccinationCount)
AS
(
SELECT dea.continent, dea.location, dea.date, dea.population, dea.new_vaccinations,
	SUM(cast(vac.new_vaccinations AS int)) OVER (PARTITION BY dea.location ORDER BY dea.location, dea.date) as RollingVaccinationCount
FROM PortfolioProject..CovidDeaths dea
JOIN PortfolioProject..CovidVaccinations vac
	ON dea.location = vac.location
	AND dea.date = vac.date
WHERE dea.continent IS NOT NULL
)
SELECT *, (RollingVaccinationCount/population)*100 AS PercentPopulationVaccinated
FROM PopvsVac

-- Temp Table

DROP TABLE if exists #PercentPopulationVaccinated
CREATE TABLE #PercentPopulationVaccinated
(
Continent nvarchar(255),
Location nvarchar(255),
Date datetime,
Population numeric,
New_Vaccinations numeric,
RollingVaccinationCount numeric
)
INSERT INTO #PercentPopulationVaccinated
SELECT dea.continent, dea.location, dea.date, dea.population, dea.new_vaccinations,
	SUM(cast(vac.new_vaccinations AS int)) OVER (PARTITION BY dea.location ORDER BY dea.location, dea.date) as RollingVaccinationCount
FROM PortfolioProject..CovidDeaths dea
JOIN PortfolioProject..CovidVaccinations vac
	ON dea.location = vac.location
	AND dea.date = vac.date
WHERE dea.continent IS NOT NULL

SELECT *, (RollingVaccinationCount/population)*100 AS PercentPopulationVaccinated
FROM #PercentPopulationVaccinated
ORDER BY 2


-- Creating View to store data for later visualizations

CREATE VIEW PercentPopulationVaccinatedView AS
SELECT dea.continent, dea.location, dea.date, dea.population, dea.new_vaccinations,
	SUM(cast(vac.new_vaccinations AS int)) OVER (PARTITION BY dea.location ORDER BY dea.location, dea.date) as RollingVaccinationCount
FROM PortfolioProject..CovidDeaths dea
JOIN PortfolioProject..CovidVaccinations vac
	ON dea.location = vac.location
	AND dea.date = vac.date
WHERE dea.continent IS NOT NULL

SELECT *
FROM PercentPopulationVaccinatedView