import { test, expect } from "@playwright/test";
import { setupClerkTestingToken, clerk } from "@clerk/testing/playwright";


test('Log in works Well', async ({ page }) => {
    await page.goto('http://localhost:5173/');
    await page.getByRole('button', { name: 'Sign In' }).click();
    await page.getByRole('textbox', { name: 'Email address or username' }).click();
    await page.getByRole('textbox', { name: 'Email address or username' }).fill('notreal');
    await page.getByRole('button', { name: 'Continue', exact: true }).click();
    await page.getByRole('textbox', { name: 'Password' }).fill('notrealnotreal');
    await page.getByRole('button', { name: 'Continue' }).click();
    await page.getByText('YouView Roster').click();
  });

test('Test on log in oyu can see possibel player picks', async ({ page }) => {
    await page.goto('http://localhost:5173/');
    await page.getByRole('button', { name: 'Sign In' }).click();
    await page.getByRole('textbox', { name: 'Email address or username' }).click();
    await page.getByRole('textbox', { name: 'Email address or username' }).fill('notreal');
    await page.getByRole('button', { name: 'Continue', exact: true }).click();
    await page.getByRole('textbox', { name: 'Password' }).fill('notrealnotreal');
    await page.getByRole('button', { name: 'Continue' }).click();
    await expect(page.getByText('Lamar JacksonQBProj: 392.22 ptsMore Info')).toBeVisible();
  });


test('On log in picking players adds them to your roster and other team rosters', async ({ page }) => {
    await page.goto('http://localhost:5173/');
    await page.getByRole('button', { name: 'Sign In' }).click();
    await page.getByRole('textbox', { name: 'Email address or username' }).click();
    await page.getByRole('textbox', { name: 'Email address or username' }).fill('notreal');
    await page.getByRole('textbox', { name: 'Email address or username' }).press('Enter');
    await page.getByRole('button', { name: 'Continue', exact: true }).click();
    await page.getByRole('textbox', { name: 'Password' }).fill('notrealnotreal');
    await page.getByRole('button', { name: 'Continue' }).click();
    await page.getByText('Jahmyr GibbsRBProj: 311.47 ptsMore Info').click();
    await page.getByRole('button', { name: 'Confirm' }).click();
    await page.getByText('Saquon BarkleyRBProj: 310.04').click();
    await page.getByRole('button', { name: 'Confirm' }).click();
    await page.getByText('Baker MayfieldQBProj: 355.83').click();
    await page.getByRole('button', { name: 'Confirm' }).click();
  });


test('test view roster works for self and others', async ({ page }) => {
    await page.goto('http://localhost:5173/');
    await page.getByRole('button', { name: 'Sign In' }).click();
    await page.locator('div').filter({ hasText: /^Email address or username$/ }).nth(2).click();
    await page.getByRole('textbox', { name: 'Email address or username' }).fill('notreal');
    await page.getByRole('button', { name: 'Continue', exact: true }).click();
    await page.getByRole('textbox', { name: 'Password' }).fill('notrealnotreal');
    await page.getByRole('button', { name: 'Continue' }).click();
    await page.getByRole('heading', { name: 'Justin Jefferson' }).click();
    await page.getByRole('button', { name: 'Confirm' }).click();
    await page.locator('div').filter({ hasText: /^YouView Roster$/ }).getByRole('button').click();
    await page.getByRole('button', { name: 'Hide Roster' }).click();
    await page.locator('div').filter({ hasText: /^Team 2View Roster$/ }).getByRole('button').click();
    await page.locator('div').filter({ hasText: /^Team 3View Roster$/ }).getByRole('button').click();
  });
