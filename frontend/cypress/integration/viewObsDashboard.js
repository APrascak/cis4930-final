describe('View OBS dashboard', function() {
    context('Actions', () => {
	beforeEach(() => {
        //cy.reload(true)
        //cy.clearLocalStorage()
        cy.visit('http://localhost:3000/account')
        //if (cy.contains('Sign Out'))
           // cy.contains('Sign Out').click()
	})

	it('Attempts to sign in user and see dashboard', () => {
        cy.visit('http://localhost:3000/signin')
        cy.get('input[name="email"]').type('qwerty@mail.com')
        cy.get('input[name="password"]').type('password')
        cy.get('button').should('be.enabled')
        cy.get('form').submit()
        //cy.get('button').click() 
        cy.visit('http://localhost:3000/account')
		
		//Valid input should result in successful login to home panel
        cy.location('pathname').should('eq', '/account')
        
        
    })
    
    it('Attempts to see OBS dashboard without signing in and gets redirected to Sign in', () => {
        cy.visit('http://localhost:3000/account')
		
		//Valid input should result in successful login to home panel
		cy.location('pathname').should('eq', '/signin')
	})
})
})

