# Changelog

## To-Do

- [ ] Settings
- [ ] Package management
    - [ ] Server support

- [ ] Import legacy media
- [ ] Remove legacy elements from models
- [ ] Forms
    + [ ] SQLite
    + [ ] JSON
- [ ] API 
- [x] Create list tables
- [x] Pagination
- [x] Search
- [ ] UX

## Unreleased

### Added

- Game list pagination
- Pywebview window management
- Javascript-based search function

### Changed

- Blueprint support.
- Migrated platform from Django to Flask.
- Images are now managed via a flat-file system instead of via database.

## [0.3.1] - 2022.0814.2023

### Added

- `alt_title`, `engine` to Game model
- Platform logos to platform game index.

## [0.3.0] 

### Added

- Loading screen
- App initializes database and app directories if not found
- Giantbomb, IGDB, ProtonDB to Links section on games.detail

### Changed

- Added `empr.py` to replace `manage.py` as main exec
- Platform is no longer a required field
- Changed browser engine to nativefier

### Removed

- Iron browser

## [0.2.0] - 2022.0812.2158

### Added

- Desktop support (Iron Browser)

### Changed

- Minor UI changes

## [0.1.0] - 2020.0811.2239

### Added
- Forms (Game, Genre, Platform, Tag) => add, edit, delete
- System messages

### Changed
- UI update
